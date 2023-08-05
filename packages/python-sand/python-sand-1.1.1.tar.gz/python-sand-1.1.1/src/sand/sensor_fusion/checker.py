from __future__ import annotations

from sand.config import SensorFusionConfig
from sand.datatypes import Box, Point
from sand.sensor_fusion.box import BoxChecker
from sand.sensor_fusion.collision import Collision
from sand.sensor_fusion.danger_zone import DangerZone
from sand.sensor_fusion.heatmap import HeatMap
from sand.sensor_fusion.person import PersonChecker
from sand.sensor_fusion.point import PointChecker


class Checker:
    heat_maps: dict[str, HeatMap] = {}
    danger_zone: dict[str, DangerZone] = {}

    def __init__(self, config: SensorFusionConfig):
        self.config = config
        self.init_data()

    def reinit_data(self, config: SensorFusionConfig) -> None:
        self.config = config
        self.init_data()

    def init_data(self) -> None:
        self.heat_maps["pointcloud"] = HeatMap(self.config)
        self.heat_maps["detection"] = HeatMap(self.config)
        self.danger_zone["object"] = DangerZone(
            self.config, self.config.danger_zones.object_polygons
        )
        self.danger_zone["person"] = DangerZone(
            self.config, self.config.danger_zones.person_polygons
        )
        self.collision = Collision(self.config, self.danger_zone)
        self.person_checker = PersonChecker(
            self.config,
            self.heat_maps["detection"],
            self.collision,
        )
        self.box_checker = BoxChecker(
            self.config,
            self.heat_maps["detection"],
            self.collision,
        )
        self.point_checker = PointChecker(
            self.heat_maps["pointcloud"],
            self.collision,
        )

    def test_box(self, box: Box) -> bool:
        return self.box_checker.test(box)

    def test_person(self, box: Box) -> bool:
        return self.person_checker.test(box)

    def test_point(self, point: Point) -> bool:
        return self.point_checker.test(point)

    def reset_collision(self) -> None:
        self.collision.reset()

    def get_collision_map(self) -> list[list[int]]:
        return self.collision.collision_map

    def get_heat_maps(self) -> dict[str, HeatMap]:
        return self.heat_maps
