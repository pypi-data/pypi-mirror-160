from __future__ import annotations

from numpy import cos, sin

from sand.config import SensorFusionConfig
from sand.datatypes import Box, Point
from sand.sensor_fusion.collision import Collision
from sand.sensor_fusion.heatmap import HeatMap
from sand.util.boxes import get_box_center


class PersonChecker:
    def __init__(
        self,
        config: SensorFusionConfig,
        heat_map: HeatMap,
        collision: Collision,
    ):
        self.collision = collision
        self.heat_map = heat_map
        self.config = config
        self.person_radius = int(self.config.scale * 75)

    def test(self, box: Box) -> bool:
        center = get_box_center(box)
        person_radius = int(self.config.scale * 75)
        collisions = 0
        for angle in range(0, 360, 10):
            point = Point(
                int(person_radius * cos(angle) + center.x * self.config.scale),
                int(person_radius * sin(angle) + center.y * self.config.scale),
            )
            self.heat_map.add_point_to_heat_map(point)
            collisions += int(self.collision.check_collision(point, "person"))
        return collisions > 0
