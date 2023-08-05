from __future__ import annotations

# disable pylint unused imports as they are used in typing hack
from copy import copy

from influxdb_client import Point
from numpy import concatenate
from overrides import overrides

from sand.config import LidarEnricherConfig, SandConfig
from sand.datatypes import EnrichedLidarPacket, LidarPoints
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import EnrichedLidarSubscriber
from sand.reader.lidar.pipeline.collector import Vlp16Collector
from sand.registry import get_nodes
from sand.util.lidar import filter_to_2d
from sand.util.per_second import PerSecondHelper
from sand.util.time import now
from sand.util.time_management import TimeManagement


class LidarPacketEnricher(SandNode, ConfigurationManager[LidarEnricherConfig]):
    def __init__(self, global_config: SandConfig) -> None:
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        self.lidar_collectors: list[Vlp16Collector] = get_nodes(Vlp16Collector)
        self.subscribers: list[EnrichedLidarSubscriber] = []
        self.pps = PerSecondHelper(self, "pps", "all", 25)
        self.time_management = TimeManagement(
            fps=25, slowdown_factor=1, shutdown_event=self.shutdown_event
        )
        self.create_thread(self.work, (), "le_all", self.config.active)

    @overrides
    def select_config(self, global_config: SandConfig) -> LidarEnricherConfig:
        return global_config.lidar_enricher

    def subscribe(self, subscriber: EnrichedLidarSubscriber) -> None:
        self.subscribers.append(subscriber)

    def work(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")
        while not self.shutdown_event.is_set():
            if not self.time_management.wait_for_next_frame():
                self.log.d("shutdown occurred", "work")
                break
            pointcloud_stats = Point("lidar_stats")
            pointcloud_stats.tag("name", "all")
            point3d_list: list[LidarPoints] = []
            point2d_list: list[LidarPoints] = []
            for lidar_collector in self.lidar_collectors:
                points3d = copy(lidar_collector.cloud.get_cloud())
                point3d_list.append(points3d)
                points2d = filter_to_2d(points3d)
                point2d_list.append(points2d)
                self.publish(
                    points2d,
                    f"{LidarPacketEnricher.__name__}/{lidar_collector.config.name}/data/pointcloud2d",
                )
            if len(point3d_list) > 0:
                points3dall: LidarPoints = concatenate(point3d_list, axis=0)
                points2dall: LidarPoints = concatenate(point2d_list, axis=0)
                packet = EnrichedLidarPacket(
                    timestamp=now(), points=points3dall, points2d=points2dall
                )
                for subscriber in self.subscribers:
                    subscriber.push_enriched_packet(packet)
                pointcloud_stats.field("point3d_count", len(points3dall))
                pointcloud_stats.field("point2d_count", len(points2dall))
            else:
                self.log.d("point3d_list is empty", "work")
            self.publish(
                pointcloud_stats.to_line_protocol(),
                f"{LidarPacketEnricher.__name__}/all/data/metric",
            )
            self.pps.inc_and_publish()
