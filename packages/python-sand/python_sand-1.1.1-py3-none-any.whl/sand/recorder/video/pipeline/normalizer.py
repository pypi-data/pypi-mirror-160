from __future__ import annotations

from time import time

from numpy import uint8, zeros
from overrides import overrides

from sand.config import CommunicationConfig
from sand.datatypes import EnrichedFrame
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import EnrichedSubscriber
from sand.reader.video import CameraSystem  # allowed
from sand.recorder.video.pipeline.writer import VideoWriter
from sand.util.per_second import PerSecondHelper
from sand.util.time import now


class VideoNormalizer(SandNode, EnrichedSubscriber):
    def __init__(
        self,
        communication_config: CommunicationConfig,
        camera_system: CameraSystem | None,
        writer: VideoWriter,
        busy_waiting_factor: int = 10,
    ) -> None:
        SandNode.__init__(self, communication_config)
        self.writer = writer

        self.frame = EnrichedFrame(
            camera_name="init",
            timestamp=now(),
            frame=zeros(shape=[1, 1, 3], dtype=uint8),
        )
        self.time_between_frames = 1 / self.writer.config.fps
        self.time_to_wait = self.time_between_frames / busy_waiting_factor
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=self.writer.config.name,
            expected=self.writer.config.fps,
        )

        self.create_thread(
            target=self.normalize,
            args=(),
            name=self._get_thread_name(),
        )

        if camera_system is not None:
            camera_system.reader.subscribe(self)

    def _get_thread_name(self) -> str:
        return f"no_{self.writer.config.name}"

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        initial = self.frame.camera_name == "init"
        self.frame = frame
        if initial:
            self.start_all_threads()

    def normalize(self) -> None:
        self.set_thread_name(f"normalizer_{self._get_thread_name()}")
        start_time = time()
        frame_count = 0

        while not self.shutdown_event.is_set():
            self.writer.push_frame(self.frame)
            frame_count += 1

            next_frame_time = start_time + frame_count * self.time_between_frames
            try:
                self.writer.stats.log_metric()
            except IndexError:
                self.log.exception("Writer thread not started yet", "normalize")

            self.fps.inc_and_publish()
            while not self.shutdown_event.is_set() and time() < next_frame_time:
                # wait on shutdown_event to recognize shutdown
                self.shutdown_event.wait(self.time_to_wait)
