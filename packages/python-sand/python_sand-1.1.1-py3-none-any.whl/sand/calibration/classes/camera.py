from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cv2 import perspectiveTransform
from nptyping import Float, NDArray, Shape
from numpy import array

from sand.calibration.image_calibration import calc_matrix
from sand.datatypes import CalPoints, Dimensions, Matrix, Point


@dataclass
class Cam:
    name: str
    image_path: Path
    focal: int
    calibration_points: CalPoints
    corner_calibration_points: CalPoints
    dimension: Dimensions

    def get_scaled_calibration_points(
        self, scale: float, corner_points: bool = False
    ) -> CalPoints:
        target_points = []
        source_points = []

        points = self.calibration_points
        if corner_points:
            points = self.corner_calibration_points
        for point in points.target_points:
            target_points.append(Point(int(point.x * scale), int(point.y * scale)))
        for point in points.source_points:
            source_points.append(Point(int(point.x * scale), int(point.y * scale)))
        return CalPoints(source_points, target_points)

    @staticmethod
    def _get_corner_transformeration_points(
        matrix: Matrix, width: int, height: int
    ) -> CalPoints:
        print(width, height, matrix.shape)  # typing: ignore
        scaled_width = int(width)
        scaled_height = int(height)
        corner_points = [
            [0, 0],
            [0, scaled_height],
            [scaled_width, scaled_height],
            [scaled_width, 0],
        ]
        np_points = array([corner_points], dtype="float32")
        target_points: NDArray[Shape["4 points, [x, y]"], Float] = perspectiveTransform(
            np_points, matrix
        )
        int_points = target_points.astype(int)[0]
        output_points = list(map(lambda pt: Point(int(pt[0]), int(pt[1])), int_points))
        source_points = list(
            map(lambda pt: Point(int(pt[0]), int(pt[1])), corner_points)
        )
        return CalPoints(target_points=output_points, source_points=source_points)

    def calc_corner_calibration_points(self) -> None:
        matrix = calc_matrix(self.calibration_points)
        self.corner_calibration_points = self._get_corner_transformeration_points(
            matrix, self.dimension.width, self.dimension.height
        )
