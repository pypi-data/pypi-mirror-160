from __future__ import annotations

from multiprocessing.shared_memory import SharedMemory
from time import time

from numpy import uint8, zeros
from overrides import overrides

from sand.config import CameraConfig, CommunicationConfig
from sand.datatypes import EnrichedFrame, Image
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import CollectAble, EnrichedSubscriber
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper
from sand.util.time import now
from sand.util.time_management import TimeManagement

from .encoder import FrameEncoder


class FrameDecoder(SandNode, CollectAble[EnrichedSubscriber]):
    def __init__(
        self,
        config: CameraConfig,
        communication_config: CommunicationConfig,
    ) -> None:
        SandNode.__init__(self, communication_config)
        self.config = config
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=self.config.name,
            expected=1,
        )

        self.subscribers: list[EnrichedSubscriber] = []
        self.source = FrameEncoder.__name__
        self.time_management = TimeManagement(1, slowdown_factor=1)
        self.cached_frame = EnrichedFrame(
            self.config.name,
            now(),
            self.__get_fail_image(self.config),
        )

        self._shared_buffer: SharedMemory | None = None
        self.log_broken_frame = self.log.d

        self.create_thread(
            target=self.decode_frames,
            name=f"fd_{self.config.name}",
            start=True,
        )

    @staticmethod
    def __get_fail_image(camera_config: CameraConfig) -> Image:
        image: Image = zeros(
            (
                camera_config.stream_resolution.height,
                camera_config.stream_resolution.width,
                3,
            ),
            dtype=uint8,
        )
        # make image red in BGR
        image[:, :, 2] = 255
        return image

    def _wait_until_shared_memory_available(
        self, timeout: int = 20
    ) -> SharedMemory | None:
        timeout_time = time() + timeout
        while not self.shutdown_event.is_set():
            try:
                return SharedMemory(name=self.config.name, create=False)
            except FileNotFoundError:
                if time() > timeout_time:
                    self.log.d(
                        f"Timeout while waiting for shared_memory for {self.config.name=}",
                        "_wait_until_shared_memory_available",
                    )
                    return None

                self.log.d(
                    f"Still waiting on shared_memory for {self.config.name=}",
                    "_wait_until_shared_memory_available",
                )
                self.shutdown_event.wait(5)  # check timeout; return on timeout

        self.log.i(
            "Shutdown while waiting on shared_memory",
            "_wait_until_shared_memory_available",
        )
        return None

    @overrides
    def subscribe(self, subscriber: EnrichedSubscriber) -> None:
        self.subscribers.append(subscriber)

    @overrides
    def shutdown(self) -> None:
        if self._shared_buffer is not None:
            self._shared_buffer.close()

    def __send(self) -> None:
        if self.cached_frame is not None:
            for subscriber in self.subscribers:
                subscriber.push_frame(self.cached_frame)

    def __try_creating_shared_memory(self) -> None:
        if self._shared_buffer is not None:
            return

        self._shared_buffer = self._wait_until_shared_memory_available()
        if self._shared_buffer is None:
            self.log.i("SharedMemory did not come up yet", "decode_frames")

    def __get_cached_frame_id(self) -> int:
        return self.cached_frame.id if self.cached_frame is not None else -1

    def decode_frames(self) -> None:
        self.set_thread_name(f"fd_{self.config.name}")
        while not self.shutdown_event.is_set():
            self.__try_creating_shared_memory()

            if not self.time_management.wait_for_next_frame():
                self.log.d("Shutdown for FrameDecoder", "decode_frames")
                break

            start = time()
            id_before = self.__get_cached_frame_id()

            try:
                if self._shared_buffer is None:
                    new_frame = False
                else:
                    self.cached_frame = EnrichedFrame.from_bytes(
                        self._shared_buffer.buf
                    )
                    new_frame = id_before != self.cached_frame.id
                    # at least one frame worked, switch log-levels
                    self.log_broken_frame = self.log.exception
            except:  # pylint: disable=bare-except
                self.log_broken_frame(
                    "exception when reading frame from buffer", "decode_frames"
                )
                new_frame = False

            self.__send()

            self.__create_delta_metric(new_frame, start)

            self.fps.inc_and_publish()

    def __create_delta_metric(self, new_frame: bool, start: float) -> None:
        if not new_frame:
            # no new frame, therefore no delta
            return

        assert self.cached_frame is not None
        delta = DeltaHelper(
            communicator=self,
            device_name=self.config.name,
            data_id=self.cached_frame.id,
            source=[self.source],
        )
        delta.set_start(start)
        delta.set_end_and_publish()
