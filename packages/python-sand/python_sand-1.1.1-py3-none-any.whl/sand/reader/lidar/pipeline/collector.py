from __future__ import annotations

from queue import Queue
from typing import Optional  # pylint: disable=unused-import

from overrides import overrides

from sand.config import LidarConfig, SandConfig
from sand.datatypes import LidarPacket
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import LidarSubscriber
from sand.reader.lidar.cloud import Vlp16Cloud
from sand.reader.lidar.pipeline.reader import LidarReader
from sand.util.per_second import PerSecondHelper
from sand.util.time import now


class Vlp16Collector(SandNode, LidarSubscriber, ConfigurationManager[LidarConfig]):
    packets_per_sec = 10 * 15
    packets_per_minute = 60 * packets_per_sec
    log_non_verbose = packets_per_minute

    def __init__(
        self, reader: LidarReader, lidar_name: str, sand_config: SandConfig
    ) -> None:
        SandNode.__init__(self, sand_config.communication)
        ConfigurationManager.__init__(self, self, sand_config)
        self._lidar_name = lidar_name

        self.queue: Queue[LidarPacket | None] = Queue()
        self.cloud = Vlp16Cloud(lidar_name, self.config.transformation)

        self.pps = PerSecondHelper(
            self,
            "pps",
            f"lidar_collector/{self.config.name}",
            self.packets_per_sec,
        )
        self._frame_counter = 0
        if self.config.active:
            self.create_thread(
                target=self.collect, args=(), name=f"lc_{self.config.name}", start=True
            )
            reader.subscribe(self)

    @overrides
    def select_config(self, global_config: SandConfig) -> LidarConfig:
        for lidar_config in global_config.lidars:
            if lidar_config.name == self._lidar_name:
                return lidar_config

        assert (
            False
        ), f"The configured name {self._lidar_name} is not in the global config"

    @overrides
    def push_packet(self, packet: LidarPacket) -> None:
        self.queue.put(packet)

    def _should_log_intermediary_stats(self) -> bool:
        return not self._frame_counter % self._log_package_count()

    def _log_package_count(self) -> int:
        if self._frame_counter < self.log_non_verbose:
            return self.packets_per_sec
        return self.packets_per_minute

    def collect(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}_collect")

        time = now()
        while not self.shutdown_event.is_set():
            packet = self.queue.get()

            if packet is None:
                self.log.i("Shutdown recognized...", "collect")
                break

            self.cloud.update_point_cloud(packet)
            self._frame_counter += 1
            if self._should_log_intermediary_stats():
                self.log.d(
                    f"{self.config.name} Queue size: {self.queue.qsize()} | "
                    f"time for {self._log_package_count()} Packages: {now() - time}",
                    "collect",
                )
                time = now()
            self.pps.inc_and_publish()

    @overrides
    def shutdown_before_join(self) -> None:
        self.queue.put(None, block=True)

    def get_cloud(self) -> Vlp16Cloud:
        return self.cloud
