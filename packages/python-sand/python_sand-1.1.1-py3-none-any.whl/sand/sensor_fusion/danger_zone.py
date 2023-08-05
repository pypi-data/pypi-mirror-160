from __future__ import annotations

from cv2 import fillPoly
from numpy import array, zeros

from sand.config import SensorFusionConfig
from sand.datatypes import Color, Image, Point


class DangerZone:
    def __init__(self, config: SensorFusionConfig, polygons: list[list[Point]]):
        self.config = config
        self.polygons = polygons
        self.danger_zone: list[list[int]] = self.build_lookup_table(polygons)

    def build_lookup_table(self, polygons: list[list[Point]]) -> list[list[int]]:
        lookup_map = self.get_empty_image()
        for poly in polygons:
            scaled_poly = []
            for point in poly:
                scaled_poly.append(
                    Point(
                        int(point.x * self.config.scale),
                        int(point.y * self.config.scale),
                    )
                )
            lookup_map = fillPoly(
                lookup_map, pts=[array(scaled_poly)], color=Color(255, 0, 0)
            )
        lookup_table = []
        for column in lookup_map:
            rows = []
            for row in column:
                rows.append(1 if row[0] == 255.0 else 0)
            lookup_table.append(rows)
        return lookup_table

    # noinspection PyTypeChecker
    def get_empty_image(self) -> Image:
        return zeros(
            (
                int(self.config.map_height * self.config.scale),
                int(self.config.map_width * self.config.scale),
                3,
            )
        )
