from __future__ import annotations

from sand.config import SensorFusionConfig
from sand.datatypes import Box, Point
from sand.sensor_fusion.collision import Collision
from sand.sensor_fusion.heatmap import HeatMap


class BoxChecker:
    def __init__(
        self,
        config: SensorFusionConfig,
        heat_map: HeatMap,
        collision: Collision,
    ):
        self.collision = collision
        self.heat_map = heat_map
        self.config = config

    def test_line(self, point_one: Point, point_two: Point) -> bool:
        point_one_scaled = Point(
            int(point_one.x * self.config.scale), int(point_one.y * self.config.scale)
        )
        point_two_scaled = Point(
            int(point_two.x * self.config.scale), int(point_two.y * self.config.scale)
        )
        ydiff = point_two_scaled.y - point_one_scaled.y
        xdiff = point_two_scaled.x - point_one_scaled.x

        # line is only one point long
        if point_one_scaled == point_two_scaled:
            try:
                self.heat_map.add_point_to_heat_map(point_one_scaled)
            except IndexError:
                pass
            return self.collision.check_collision(point_one_scaled)

        diff = ydiff
        if abs(xdiff) > abs(ydiff):
            diff = xdiff

        offsets = range(0, diff + 1)
        if diff < 0:
            offsets = range(diff, 1)

        for offset in offsets:
            xoffset = offset
            yoffset = offset
            if abs(xdiff) > abs(ydiff):
                yoffset = int(ydiff / xdiff * offset)
            else:
                xoffset = int(xdiff / ydiff * offset)
            point = Point(point_one_scaled.x + xoffset, point_one_scaled.y + yoffset)
            try:
                self.heat_map.add_point_to_heat_map(point_one_scaled)
            except IndexError:
                pass
            if self.collision.check_collision(point):
                return True
        return False

    def test(self, box: Box) -> bool:
        return any(
            [
                self.test_line(box.upper_left, box.upper_right),
                self.test_line(box.upper_right, box.lower_right),
                self.test_line(box.lower_right, box.lower_left),
                self.test_line(box.lower_left, box.upper_left),
            ]
        )
