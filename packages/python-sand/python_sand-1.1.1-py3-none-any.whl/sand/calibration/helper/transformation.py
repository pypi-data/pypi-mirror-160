from __future__ import annotations

import sys
from ast import literal_eval

from cv2 import getPerspectiveTransform
from numpy import float32

from sand.config import SandConfig
from sand.config.config import _to_points
from sand.datatypes import CalPoints, Matrix


def calc_matrix(points: CalPoints) -> Matrix:
    if len(points.target_points) == 4 and len(points.source_points) == 4:
        return getPerspectiveTransform(  # type: ignore[no-any-return]
            float32(points.source_points), float32(points.target_points)  # type: ignore[arg-type]
        )
    print("error")
    print(f"points.target_points {points.target_points}")
    print(f"points.source_points {points.source_points}")
    sys.exit(2)


def calibration_points_from_id(sand_config: SandConfig, camera_id: int) -> CalPoints:
    return CalPoints(
        source_points=_to_points(
            literal_eval(sand_config.cameras[camera_id].transformation_source_points)
        ),
        target_points=_to_points(
            literal_eval(sand_config.cameras[camera_id].transformation_target_points)
        ),
    )
