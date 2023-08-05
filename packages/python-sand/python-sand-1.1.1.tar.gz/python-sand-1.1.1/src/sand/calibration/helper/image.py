from __future__ import annotations

from datetime import datetime

from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    bitwise_not,
    bitwise_or,
    cvtColor,
    imread,
    threshold,
    warpPerspective,
)

from sand.config import SandConfig, get_camera_id
from sand.datatypes import CalPoints, Color, EnrichedFrame, Image, Matrix, Point
from sand.transformer.focal import FocalNormalizer  # allowed
from sand.util.camera import get_path_from_camera_name
from sand.util.image import crop_image_on_map, draw_x

from .transformation import calc_matrix, calibration_points_from_id


def add_image_to_map(
    sand_config: SandConfig, name: str, map_image: Image, width: int, height: int
) -> Image:
    cam_id = get_camera_id(sand_config, name)
    points = calibration_points_from_id(sand_config, cam_id)
    matrix: Matrix = calc_matrix(points)
    image = imread(get_path_from_camera_name(name).as_posix())
    print(name, "image size:", image.shape)
    enriched_frame = EnrichedFrame("image", datetime.now(), image)
    undistorted_image = FocalNormalizer(
        sand_config.cameras[cam_id].focal
    ).normalize_image(enriched_frame.frame)
    warped_image = warpPerspective(undistorted_image, matrix, (width, height))
    cropped_image = crop_image_on_map(
        image=warped_image,
        name=name,
        target_width=width,
        target_height=height,
    )
    _th, mask = threshold(
        cvtColor(cropped_image, COLOR_BGR2GRAY), 3, 255, THRESH_BINARY
    )
    return cropped_image + bitwise_or(map_image, map_image, mask=bitwise_not(mask))  # type: ignore[no-any-return]


def draw_calibration_points(
    map_image: Image,
    points: CalPoints,
    active_point_index: int = -1,
    draw_source: bool = False,
) -> Image:
    def draw(map_image: Image, points: list[Point]) -> None:
        for pid, point in enumerate(points):
            if pid == active_point_index:
                map_image = draw_x(
                    map_image, point.x, point.y, Color(255, 0, 0), line_width=4, size=50
                )
            else:
                map_image = draw_x(
                    map_image, point.x, point.y, Color(0, 0, 0), line_width=4, size=50
                )

    if draw_source:
        draw(map_image, points.source_points)
    draw(map_image, points.target_points)
    return map_image


def draw_active_calibration_point(map_image: Image, point: Point) -> None:
    draw_x(map_image, point.x, point.y, Color(255, 0, 0), line_width=2)
