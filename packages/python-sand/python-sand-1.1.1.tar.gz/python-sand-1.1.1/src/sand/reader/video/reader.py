from __future__ import annotations

from datetime import datetime, timedelta
from time import time
from typing import Any

from cv2 import CAP_PROP_BUFFERSIZE, CAP_PROP_FOURCC, VideoCapture, VideoWriter_fourcc
from cv2 import error as CVError
from cv2 import imread
from overrides import overrides

from sand.config import CameraConfig, CommunicationConfig
from sand.datatypes import EnrichedFrame, Image
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import CollectAble, EnrichedSubscriber
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper
from sand.util.time import now

from .stats import ReaderStatistics


class ImageCapture(VideoCapture):
    image: Image

    def __init__(self, path: str, *args: Any, **kwargs: Any) -> None:
        self.image = imread(path)
        super().__init__(*args, **kwargs)

    def isOpened(self) -> bool:  # pylint: disable=invalid-name
        return True

    def set(self, *args: Any) -> None:
        pass

    def release(self) -> None:
        pass

    def getExceptionMode(self) -> str:  # pylint: disable=invalid-name
        return "static jpeg mode"

    def grab(self) -> bool:
        return True

    def retrieve(
        self, image: Any = None, flag: Any = None  # pylint: disable=unused-argument
    ) -> tuple[bool, Image]:
        return True, self.image


class CameraReader(SandNode, CollectAble[EnrichedSubscriber]):
    def __init__(
        self,
        config: CameraConfig,
        communication_config: CommunicationConfig,
        playback: bool,
    ) -> None:
        SandNode.__init__(self, communication_config)
        self.config = config
        self.subscribers: list[EnrichedSubscriber] = []
        # log intermediary statistic every {self.fps}-frames in the first minute
        self.verbose_log_frame_count = self.config.fps * 60

        # after that log them once every 10 minutes
        self.non_verbose_log_frame_count = self.config.fps * 60 * 10

        self.playback = playback
        self.next_metric: datetime

        self.stats = ReaderStatistics(self.config, self)

        self.create_thread(
            target=self._open_camera,
            args=(),
            name=f"r_{self.config.name}",
            start=False,
        )

        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=self.config.name,
            expected=self.config.fps,
        )

    def start(self) -> None:
        self.start_all_threads()

    @overrides
    def subscribe(self, subscriber: EnrichedSubscriber) -> None:
        self.subscribers.append(subscriber)

    def _should_log_intermediary_stats(self) -> bool:
        if self.stats.recorded_frames < self.verbose_log_frame_count:
            return not self.stats.recorded_frames % self.config.fps

        return not self.stats.recorded_frames % self.non_verbose_log_frame_count

    def get_stream(self) -> str | int:
        try:
            return int(self.config.stream)
        except ValueError:
            return self.config.stream

    def _open_camera(self) -> None:
        self.set_thread_name(f"CR_{self.config.name}")
        fct = "open_cam"
        try:
            while not self.shutdown_event.is_set():
                if self.config.stream.endswith(".jpg"):
                    self.log.d(
                        f"Opening stream with ImageCapture: {self.config.stream}", fct
                    )
                    stream = ImageCapture(self.config.stream)
                else:
                    self.log.d(
                        f"Opening stream with VideoCapture: {self.config.stream}", fct
                    )
                    stream = VideoCapture(self.get_stream())

                if not stream.isOpened():
                    self.log.w(f"Error when opening stream: {self.config.stream}", fct)
                    self.shutdown_event.wait(1)
                    continue

                stream_buffer_size = 1
                stream.set(CAP_PROP_BUFFERSIZE, stream_buffer_size)
                stream.set(CAP_PROP_FOURCC, VideoWriter_fourcc("M", "J", "P", "G"))

                (
                    successful_grab,
                    successful_retrieve,
                ) = self._record_stream(stream)

                stream.release()

                if not successful_grab or not successful_retrieve:
                    self.log.w(
                        "Stream could not read frame, increasing dropped_frames and trying again, "
                        f"successful_grab: {successful_grab} | successful_retrieve: {successful_retrieve}",
                        fct,
                    )
                    self.stats.add_dropped_frame()
                self.stats.log_metric()
                self.fps.inc_and_publish()
        except CVError:
            self.log.exception("Critical error while reading from camera", fct)
        self.log.w(f"Shutting down CameraReader for {self.config.name}", fct)
        self.stats.log_metric()

    def _record_stream(self, stream: VideoCapture | ImageCapture) -> tuple[bool, bool]:
        successful_retrieve = True
        successful_grab = True
        segment_start = now()
        self.next_metric = now() + timedelta(seconds=self.config.metric_interval)
        while (
            successful_grab and successful_retrieve and not self.shutdown_event.is_set()
        ):

            before_grab = now()
            successful_grab = stream.grab()
            after_grab = now()
            successful_retrieve, frame = stream.retrieve()

            after_retrieve = now()

            if successful_grab and successful_retrieve:
                enriched_frame = EnrichedFrame(self.config.name, now(), frame)
                delta = DeltaHelper(
                    communicator=self,
                    device_name=self.config.name,
                    data_id=enriched_frame.id,
                    source=["none"],
                )
                delta.set_start(after_retrieve.timestamp())
                for subscriber in self.subscribers:
                    subscriber.push_frame(enriched_frame)
                delta.set_end_and_publish()

            self.stats.add_grab_time(after_grab - before_grab)
            self.stats.add_retrieve_time(after_retrieve - after_grab)
            self.stats.add_frame()

            if self._should_log_intermediary_stats():
                self.stats.log_statistics(successful_grab, successful_retrieve, stream)

            # for playback we will force the reader to $fps
            if self.playback:
                next_frame_time = (
                    segment_start.timestamp()
                    + self.stats.recorded_frames * 1 / self.config.fps
                )

                while time() < next_frame_time and not self.shutdown_event.is_set():
                    # wait on shutdown_event to recognize shutdown
                    self.shutdown_event.wait(1 / self.config.fps / 10)

            self.stats.time_for_one_frame = now() - before_grab

            if now() > self.next_metric:
                self.stats.log_metric()
                self.next_metric = now() + timedelta(
                    seconds=self.config.metric_interval
                )
        return successful_grab, successful_retrieve
