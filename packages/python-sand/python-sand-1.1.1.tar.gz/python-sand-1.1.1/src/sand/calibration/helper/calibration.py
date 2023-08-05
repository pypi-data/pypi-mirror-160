from __future__ import annotations

import sys
from ast import literal_eval
from datetime import datetime
from pathlib import Path

from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    bitwise_not,
    bitwise_or,
    cvtColor,
    getPerspectiveTransform,
    imread,
    threshold,
    warpPerspective,
)
from numpy import float32

from sand.config import SandConfig, get_camera_id
from sand.config.config import _to_points
from sand.datatypes import CalPoints, Color, EnrichedFrame, Image, Matrix, Point
from sand.reader.lidar import LidarSystem  # allowed
from sand.transformer.focal import FocalNormalizer  # allowed
from sand.util.camera import get_path_from_camera_name
from sand.util.image import crop_image_on_map, draw_x


def calc_matrix(points: CalPoints) -> Matrix:
    if len(points.target_points) == 4 and len(points.source_points) == 4:
        return getPerspectiveTransform(  # type: ignore[no-any-return]
            float32(points.source_points), float32(points.target_points)  # type: ignore[arg-type]
        )
    sys.exit(2)


def calibration_points_from_id(config: SandConfig, camera_id: int) -> CalPoints:
    return CalPoints(
        source_points=_to_points(
            literal_eval(config.cameras[camera_id].transformation_source_points)
        ),
        target_points=_to_points(
            literal_eval(config.cameras[camera_id].transformation_target_points)
        ),
    )


def add_image_to_map(
    config: SandConfig, name: str, map_image: Image, width: int, height: int
) -> Image:
    cam_id = get_camera_id(config, name)
    points = calibration_points_from_id(config, cam_id)
    matrix: Matrix = calc_matrix(points)
    image = imread(get_path_from_camera_name(name).as_posix())
    enriched_frame = EnrichedFrame("image", datetime.now(), image)
    undistorted_image = FocalNormalizer(config.cameras[cam_id].focal).normalize_image(
        enriched_frame.frame
    )
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


def draw_active_calibration_point(map_image: Image, point: Point) -> None:
    draw_x(map_image, point.x, point.y, Color(255, 0, 0), line_width=2)


def get_packets(file_path: Path, lidar_name: str, number: int) -> list[bytes]:
    if file_path == "":
        return []
    possible_files = list(file_path.joinpath(lidar_name).glob("*f1_l1_la.velo"))
    if len(possible_files) == 1:
        with open(possible_files[0], "rb") as file:
            packets: list[bytes] = []
            for _ in range(number):
                data = file.read(1210)
                if data[1206:] == b"DUDE":
                    packets.append(data[:1206])
            return packets
    return []


def init_lidar(config: SandConfig) -> list[LidarSystem]:
    lidar_systems: list[LidarSystem] = []
    for lidar_config in config.lidars:
        lidar_systems.append(
            LidarSystem(lidar_config, is_playback=True, sand_config=config)
        )
    return lidar_systems


def shutdown_lidar(lidar_systems: list[LidarSystem]) -> None:
    for lidar in lidar_systems:
        lidar.reader.shutdown()
        lidar.collector.shutdown()
