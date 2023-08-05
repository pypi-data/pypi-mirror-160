from __future__ import annotations

from pathlib import Path
from queue import Queue
from typing import BinaryIO

from overrides import overrides

from sand.config import CommunicationConfig, LidarConfig
from sand.datatypes import LidarPacket, Topic
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import LidarSubscriber
from sand.reader.lidar import LidarSystem  # allowed
from sand.util.per_second import PerSecondHelper
from sand.util.time import now


class LidarRecorder(LidarSubscriber, SandNode):
    __DEFAULT_PATH = Path("/tmp")

    def __init__(
        self,
        lidar_system: LidarSystem,
        config: LidarConfig,
        communication_config: CommunicationConfig,
        playback: bool = False,
    ) -> None:
        SandNode.__init__(self, communication_config)
        self.queue: Queue[LidarPacket | None] = Queue()
        self.config = config
        self.playback = playback
        self.write_folder = self.__DEFAULT_PATH
        self.active_folder = self.__DEFAULT_PATH
        self.lidar_system = lidar_system
        self.pps = PerSecondHelper(self, "pps", self.config.name, 150)
        self.create_thread(
            target=self.writer, args=(), name=f"lw_{self.config.name}", start=False
        )

        self.subscribe_topic("DriveWatcher/all/data/segment", self.path_change)

    def writer(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}_writer")
        count = 0
        packets_per_sec = 10 * 15
        log_seconds = 60 * 10
        log_every = log_seconds * packets_per_sec
        time = now()
        file: BinaryIO | None = None
        try:
            while not self.shutdown_event.is_set():
                if file is None or self.write_folder != self.active_folder:
                    self.log.d(
                        f"{self.config.name} Folder Change | Queue size: {self.queue.qsize()}",
                        "recorder",
                    )
                    self.active_folder = self.write_folder

                    if file is not None:
                        file.close()

                    file = open(  # pylint: disable=consider-using-with
                        self.active_folder.joinpath(
                            f"{now().timestamp()}_{self.config.name}.velo"
                        ).as_posix(),
                        "bw+",
                    )

                packet = self.queue.get()

                if packet is None:
                    break

                # the packet is the original packet from the lidar, nothing changed
                file.write(packet.packet)  # 1206 bytes long
                # i think its cool to check for an keyword after every package.
                file.write(b"DUDE")  # 4 bytes long
                count += 1
                self.pps.inc_and_publish()

                if count > log_every:
                    self.log.d(
                        f"{self.config.name} Queue size: {self.queue.qsize()} | seconds: {log_seconds} | "
                        f"time for {log_every} Packages: {now() - time}",
                        "recorder",
                    )
                    time = now()
                    count = 0
        except Exception:  # pylint: disable=broad-except
            self.log.exception("Exception while writing lidar-data", "writer")
        finally:
            if file is not None:
                file.close()

    @overrides
    def push_packet(self, packet: LidarPacket) -> None:
        self.queue.put(packet)

    def path_change(self, _: Topic, absolute_path: str) -> None:
        folder = Path(absolute_path)
        self.write_folder = folder.joinpath(self.config.name)
        self.write_folder.mkdir(parents=True, exist_ok=True)
        thread = self.get_thread(f"lw_{self.config.name}")
        if not self.config.writer_active:
            self.log.d("writer not active", "path_change")
        elif thread is not None and not thread.is_alive():
            self.log.i("start the writer thread", "path_change")
            self.lidar_system.reader.subscribe(self)
            thread.start()
        elif thread is not None:
            self.log.d(f"thread alive {thread.is_alive()}", "path_change")
            self.log.d(f"thread is not None {thread is not None}", "path_change")
        else:
            self.log.d("thread is None!", "path_change")
        self.log.d(f"changing to new folder: {folder}, time: {now()}", "path_change")

    @overrides
    def shutdown_before_join(self) -> None:
        self.queue.put(None, block=True)
