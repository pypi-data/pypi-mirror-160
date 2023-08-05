from __future__ import annotations

from collections import deque
from multiprocessing.shared_memory import SharedMemory
from threading import Event, Lock
from typing import Deque

from overrides import overrides

from sand.config import CameraConfig, CommunicationConfig
from sand.datatypes import Dimensions, EnrichedFrame
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import EnrichedSubscriber
from sand.reader.video.reader import CameraReader
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper
from sand.util.time_management import TimeManagement


def _calculate_frame_size_in_bytes(
    stream_resolution: Dimensions,
    color_size: int = 3,
) -> int:
    return stream_resolution.height * stream_resolution.width * color_size


class FrameEncoder(SandNode, EnrichedSubscriber):
    def __init__(
        self,
        config: CameraConfig,
        communication_config: CommunicationConfig,
        reader: CameraReader,
    ):
        SandNode.__init__(self, communication_config)
        self.config = config
        self.queue: Deque[EnrichedFrame] = deque(maxlen=1)
        self.time_management = TimeManagement(1, slowdown_factor=1)
        self.queue_lock = Lock()
        self.source = CameraReader.__name__
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=self.config.name,
            expected=1,
        )
        self.dropped = PerSecondHelper(
            communicator=self,
            name="dropped",
            device=self.config.name,
            expected=1,
        )
        reader.subscribe(self)

        self._shared_buffer: SharedMemory | None = None

        self.create_thread(
            target=self.encode_frames,
            name=f"fe_{self.config.name}",
            start=False,
        )

        self._initializing_shared_memory = Event()
        self.log.i(
            f"FrameEncoder is up for {self.config.name=}, waiting for first image...",
            "__init__",
        )

    def _create_shared_buffer(self, name: str, buffer_size: int) -> SharedMemory:
        try:

            shared_memory = SharedMemory(
                name=name,
                create=True,  # FrameEncoder is responsible for deleting this
                size=buffer_size,
            )
            self.log.d(f"shared_memory created for {name}", "_create_shared_buffer")
            return shared_memory
        except FileExistsError:
            self.log.w(
                f"Existing shared_memory found: {name=}",
                "_create_shared_buffer",
            )
            # delete existing as it could be different size
            existing_memory = SharedMemory(name=name, create=False)
            existing_memory.unlink()

            shared_memory = SharedMemory(
                name=name,
                create=True,  # FrameEncoder is responsible for deleting this
                size=buffer_size,
            )
            self.log.d(f"shared_memory created for {name}", "_create_shared_buffer")
            return shared_memory

    @staticmethod
    def _calculate_buffer_size(stream_resolution: Dimensions) -> int:
        return (
            _calculate_frame_size_in_bytes(stream_resolution)
            + EnrichedFrame.FRAME_OFFSET
        )

    @overrides
    def shutdown(self) -> None:
        self.log.i(
            f"Shutdown called for {self.__class__.__name__} / {self.config.name}",
            "shutdown",
        )
        try:
            if self._shared_buffer is not None:
                self._shared_buffer.unlink()
        except FileNotFoundError:
            self.log.exception("Error when trying to destroy shared_buffer", "shutdown")

        SandNode.shutdown(self)

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        with self.queue_lock:
            self.dropped.add(float(len(self.queue)))
            self.queue.append(frame)

        if (
            self._shared_buffer is None
            and not self._initializing_shared_memory.is_set()
        ):
            self._initializing_shared_memory.set()
            dimensions = Dimensions(frame.width, frame.height)

            self.log.d(
                f"FrameEncoder for {self.config.name=} is initializing with {dimensions=}",
                "push_frame",
            )

            self._shared_buffer = self._create_shared_buffer(
                self.config.name,
                FrameEncoder._calculate_buffer_size(dimensions),
            )
            self.start_all_threads()

    def encode_frames(self) -> None:
        assert self._shared_buffer is not None
        self.set_thread_name(f"fe_{self.config.name}")

        while not self.shutdown_event.is_set():
            if not self.time_management.wait_for_next_frame():
                self.log.d("Shutdown for camera_system", "encode_frames")
                break

            try:
                with self.queue_lock:
                    frame = self.queue.popleft()
                delta = DeltaHelper(
                    communicator=self,
                    device_name=self.config.name,
                    data_id=frame.id,
                    source=[self.source],
                )
                self._shared_buffer.buf[:] = frame.to_bytes()
                self.fps.inc_and_publish()
                delta.set_end_and_publish()
            except IndexError:
                # queue is empty, but we don't really care
                pass
            except ValueError:
                self.log.exception(
                    f"Error probably from early shutdown | {frame=} | "
                    "check if stream_resolution is correctly setup",
                    "encode_frames",
                )
            self.dropped.publish()
