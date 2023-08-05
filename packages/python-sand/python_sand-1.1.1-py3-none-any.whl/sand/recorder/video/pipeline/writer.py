from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path
from queue import Queue
from threading import Thread

from cv2 import VideoWriter as CV2VideoWriter
from cv2 import VideoWriter_fourcc
from overrides import overrides

from sand.config import CameraConfig, CommunicationConfig
from sand.datatypes import EnrichedFrame, Topic
from sand.datatypes.types import Point
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import EnrichedSubscriber
from sand.util.image import add_text_to_image
from sand.util.per_second import PerSecondHelper
from sand.util.time import now

from .stats import VideoRecorderStatistics, VideoWriterThreadStatistics


class _InterestingInterval:
    def __init__(
        self,
        config: CameraConfig,
    ) -> None:
        self.frames_before = config.is_interesting_before * config.fps

        self._delta_before = timedelta(seconds=config.is_interesting_before)
        self._delta_after = timedelta(seconds=config.is_interesting_after)

        self.interesting_time_frame = [now(), now()]

    def set(self, timestamp: datetime) -> bool:
        """
        Sets a new interval or extends the current interval, depending if {timestamp} is in
        the current interval or not.
        :return: True if interval is completely new, False if it was just extended
        """
        if self.is_interesting(timestamp):
            # timestamp is interesting, therefore in between the interval -> expand interval
            self.interesting_time_frame[1] = timestamp + self._delta_after
            return False

        self.interesting_time_frame = [
            timestamp - self._delta_before,
            timestamp + self._delta_after,
        ]
        return True

    def is_interesting(self, timestamp: datetime) -> bool:
        before, after = self.interesting_time_frame
        return bool(before <= timestamp <= after)


class _VideoWriterLogConfig:
    def __init__(self, fps: int) -> None:
        self.fps = fps
        # log intermediary statistic every {self.config.fps}-frames in the first minute
        self.verbose_intermediary_frame_count = self.fps * 60
        # after that log them once every 10 minutes
        self.non_verbose_intermediary_frame_count = self.fps * 60 * 10

    def should_log(self, frame_count: int) -> bool:
        if frame_count < self.verbose_intermediary_frame_count:
            return not frame_count % self.fps

        return not frame_count % self.non_verbose_intermediary_frame_count


class VideoWriter(
    SandNode,
    EnrichedSubscriber,
):
    __DEFAULT_PATH = Path("/tmp")

    codec = VideoWriter_fourcc(*"mp4v")

    def __init__(
        self,
        config: CameraConfig,
        communication_config: CommunicationConfig,
        playback: bool,
    ) -> None:
        SandNode.__init__(self, communication_config)

        self.config = config
        self.frame_queue: Queue[EnrichedFrame | None] = Queue()
        self.write_folder = self.__DEFAULT_PATH
        self.playback = playback

        self.stats = VideoRecorderStatistics(self.config, self)
        self.intermediary_log_config = _VideoWriterLogConfig(self.config.fps)
        self.interesting_interval = _InterestingInterval(self.config)
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=self.config.name,
            expected=self.config.fps,
        )

        self.create_thread(
            target=self.write,
            args=(),
            name=f"{self.config.name}_{len(self._threads)}",
        )

        self.subscribe_topic("DriveWatcher/all/data/segment", self.path_change)

        if self.config.interesting_mode == "off":
            self.log.i(
                f"[{self.config.name}] Configured to be always interesting, recording everything",
                "__init__",
            )
            self._is_interesting = lambda *_, **__: True  # type: ignore[assignment]
            self.interesting_interval.frames_before = sys.maxsize
        else:
            self.log.i(
                f"[{self.config.name}] Interesting mode configured, recording spots",
                "__init__",
            )
            self.subscribe_topic("+/+/data/interesting", self.__on_interesting_message)

    def _get_current_thread_name(self) -> str:
        return f"{self.config.name}_{len(self._threads) - 1}"

    def _get_current_thread(self) -> Thread:
        current_thread = self.get_thread(self._get_current_thread_name())
        assert (
            current_thread is not None
        ), f"Could not find current thread under name {self._get_current_thread_name()}"
        return current_thread

    def __on_interesting_message(self, _: Topic, timestamp: datetime) -> None:
        self.set_interesting(timestamp)

    def set_interesting(self, timestamp: datetime) -> None:
        self.interesting_interval.set(timestamp)

        current_thread = self._get_current_thread()
        if not current_thread.is_alive():
            # something interesting happened and the recorder is not running
            self.log.i(
                f"[{self.config.name}] interesting timestamp: {timestamp} | starting recorder thread",
                "set_interesting",
            )
            current_thread.start()
        else:
            self.log.d(
                f"[{self.config.name}] interesting: {timestamp} | thread already running",
                "set_interesting",
            )

    # we are not really hiding this method, but overriding it with a lambda returning True if needed
    def _is_interesting(  # pylint: disable=method-hidden
        self, timestamp: datetime
    ) -> bool:
        return self.interesting_interval.is_interesting(timestamp)

    def _replace_thread(self) -> Thread:
        self.frame_queue.put(None)
        self.frame_queue = Queue()
        return self.create_thread(
            target=self.write,
            args=(),
            name=f"{self.config.name}_{len(self._threads)}",
        )

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        if self.frame_queue.qsize() > self.interesting_interval.frames_before:
            self.frame_queue.get(block=False)

        self.frame_queue.put(frame)

    def path_change(self, _: Topic, absolute_path: str) -> None:
        self.write_folder = Path(absolute_path).joinpath(self.config.name)
        self.write_folder.mkdir(parents=True, exist_ok=True)

        self.log.d(
            f"[{self.config.name}] changing to new folder: {self.write_folder.as_posix()}, time: {now()}",
            "path_change",
        )

        current_thread = self._get_current_thread()
        if current_thread.is_alive():
            replacement_thread = self._replace_thread()
            self.log.d(
                f"[{self.config.name}] Thread was running before, therefore start again",
                "path_change",
            )
            replacement_thread.start()
        elif not current_thread.is_alive() and self.config.interesting_mode == "off":
            self.log.d(
                f"[{self.config.name}] Configured always interesting, starting initial thread",
                "path_change",
            )
            current_thread.start()

    def _create_video_writer_setup(
        self,
        frame_queue: Queue[EnrichedFrame | None],
    ) -> tuple[CV2VideoWriter, VideoWriterThreadStatistics, float] | None:
        enriched = frame_queue.get()

        if enriched is None:
            return None

        thread_stats = self.stats.new_writer_stats(self.write_folder)

        self.log.d(
            f"[{self.config.name}] Writing to file: {thread_stats.path_to_segment_file}",
            "_create_video_writer_setup",
        )

        height, width = enriched.frame.shape[:2]
        font_scale = VideoWriter.get_font_scale(width)

        writer = CV2VideoWriter(
            thread_stats.path_to_segment_file.as_posix(),
            VideoWriter.codec,
            self.config.fps,
            (width, height),
        )

        is_frame_handled = self._handle_frame(writer, enriched, font_scale)

        if not is_frame_handled:
            self._replace_thread()
            writer.release()
            return None

        return writer, thread_stats, font_scale

    def _handle_frame(
        self,
        writer: CV2VideoWriter,
        enriched: EnrichedFrame,
        font_scale: float,
    ) -> bool:
        if not self._is_interesting(enriched.timestamp):
            self.log.d(
                "Frame is not interesting, report it to writer thread",
                "_handle_frame",
            )
            return False

        local_frame = add_text_to_image(
            enriched.frame,
            str(enriched.timestamp),
            Point(0, 50),
            font_scale=font_scale,
            thickness=2,
        )

        if not self.playback:
            writer.write(local_frame)

        return True

    def write(self) -> None:
        self.set_thread_name(f"{self._get_current_thread_name()}_{self.log.name}")
        fct = "write"

        local_queue = self.frame_queue

        setup = self._create_video_writer_setup(local_queue)

        if setup is None:
            self.log.w(
                f"[{self.config.name}] writer not created, assuming fast shutdown",
                fct,
            )
            return

        writer, thread_stats, font_scale = setup
        thread_stats.start_segment = now()

        while True:
            enriched = local_queue.get()

            if enriched is None:
                # either shutdown or segment change
                break

            is_frame_handled = self._handle_frame(writer, enriched, font_scale)
            if not is_frame_handled:
                # not interesting, therefore stop writer and replace it
                self._replace_thread()
                break

            thread_stats.frame_count += 1
            thread_stats.queue_count += local_queue.qsize()

            if self.intermediary_log_config.should_log(thread_stats.frame_count):
                self.log.d(
                    f"[{thread_stats.file_name}] frame_count: {thread_stats.frame_count} | "
                    f"queue_size: {local_queue.qsize()}",
                    fct,
                )
            self.stats.log_metric()
            self.fps.inc_and_publish()
        thread_stats.end_segment = now()
        writer.release()

        self.log_final_statistics(thread_stats)

    def log_final_statistics(self, thread_stats: VideoWriterThreadStatistics) -> None:
        thread_stats.log_statistics()
        thread_stats.log_metric()
        fps = (
            thread_stats.frame_count
            / (thread_stats.end_segment - thread_stats.start_segment).total_seconds()
        )
        self.log.d(
            (
                f"[{thread_stats.file_name}] start: {thread_stats.start_segment} | "
                f"end: {thread_stats.end_segment} | frames: {thread_stats.frame_count} | "
                f"diff: {thread_stats.end_segment - thread_stats.start_segment} | fps: {fps} | "
                f"mean_queue_count: {thread_stats.get_mean_queue_count()}"
            ),
            "log_final_statistics",
        )
        self.stats.remove_writer_stats(thread_stats)

    @overrides
    def shutdown_before_join(self) -> None:
        self.frame_queue.put(None, block=True)

    @staticmethod
    def get_font_scale(width: int) -> float:
        return float(width / 1280)
