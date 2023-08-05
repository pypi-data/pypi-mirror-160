from __future__ import annotations

from numpy import zeros

from sand.config import SensorFusionConfig
from sand.datatypes import CollisionMap, LidarPoints, Point, Topic, TransformedBoxes
from sand.sensor_fusion.danger_zone import DangerZone


class Collision:
    boxes: dict[Topic, TransformedBoxes] = {}
    pointcloud2d: dict[str, LidarPoints] = {}

    def __init__(self, config: SensorFusionConfig, danger_zones: dict[str, DangerZone]):
        self.danger_zones = danger_zones
        self.config = config
        self.reset()

    def reset(self) -> None:
        self.collision_map = self.get_empty_collision_map()

    def check_collision(self, point: Point, danger_zone_type: str = "object") -> bool:
        if (
            0 <= point.y < len(self.danger_zones[danger_zone_type].danger_zone)
            and 0
            <= point.x
            < len(self.danger_zones[danger_zone_type].danger_zone[point.y])
            and (self.danger_zones[danger_zone_type].danger_zone[point.y][point.x])
        ):
            self.collision_map[point.y][point.x] = True
            return True
        return False

    def get_empty_collision_map(self) -> CollisionMap:
        return zeros(  # type: ignore[no-any-return]
            (
                int(self.config.map_height * self.config.scale),
                int(self.config.map_width * self.config.scale),
            ),
            dtype=int,
        ).tolist()
