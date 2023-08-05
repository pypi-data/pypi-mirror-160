from __future__ import annotations

from sand.datatypes import Point
from sand.sensor_fusion.collision import Collision
from sand.sensor_fusion.heatmap import HeatMap


class PointChecker:
    def __init__(
        self,
        heat_map: HeatMap,
        collision: Collision,
    ):
        self.collision = collision
        self.heat_map = heat_map

    def test(self, point: Point) -> bool:
        self.heat_map.add_point_to_heat_map(
            Point(point.x, point.y),
        )
        return self.collision.check_collision(point, "object")
