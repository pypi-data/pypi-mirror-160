from __future__ import annotations

import sys
from argparse import ArgumentParser
from copy import copy
from typing import Any

import yaml
from cv2 import (
    BORDER_CONSTANT,
    EVENT_LBUTTONDOWN,
    EVENT_MBUTTONDOWN,
    EVENT_RBUTTONDOWN,
    LINE_AA,
    WINDOW_NORMAL,
    copyMakeBorder,
    destroyAllWindows,
    getPerspectiveTransform,
    imread,
    imshow,
    namedWindow,
    setMouseCallback,
    startWindowThread,
    waitKey,
)
from numpy import float32

from sand.config import (
    get_basic_transformer_combination_config,
    get_camera_id,
    get_config,
)
from sand.datatypes import CalPoints, Color, Image, Matrix, Point
from sand.transformer.transformation import Transformation  # allowed
from sand.util.camera import get_path_from_camera_name
from sand.util.image import add_text_to_image, draw_x, split_image

BORDERSIZE = 300

CAMERA_NAME = ""
CAMERA_ID = 0
FILE_PATH = ""
point_list: list[Point] = []


class Counter:
    source_click: int = 0
    target_click: int = 0


def calc_matrix(points: CalPoints) -> Matrix:
    if len(points.target_points) == 4 and len(points.source_points) == 4:
        return getPerspectiveTransform(  # type: ignore[no-any-return]
            float32(points.source_points),  # type: ignore[arg-type]
            float32(points.target_points),  # type: ignore[arg-type]
        )
    print("error")
    print(f"points.target_points {points.target_points}")
    print(f"points.source_points {points.source_points}")
    sys.exit(2)


def print_calibration_data(points: CalPoints) -> None:
    print("")
    print("----------------------------")
    print("cameras data")
    print("")
    print(f"source points: {points.source_points}")
    print(f"target points: {points.target_points}")
    print(f"transformation matrix: {calc_matrix(points)}")
    print("----------------------------")


def find_nearest_point(left: int, top: int) -> Point:
    nearest_point = Point(-99999, -99999)
    for point in point_list:
        diff_x = abs(point.x - left)
        diff_y = abs(point.y - top)
        if diff_x <= abs(nearest_point.x - left) and diff_y <= abs(
            nearest_point.y - top
        ):
            nearest_point = point
    print(f"found nearest {nearest_point} for Input({left},{top})")

    diff_x = abs(nearest_point.x - left)
    diff_y = abs(nearest_point.y - top)
    if diff_x > 100 or diff_y > 100:
        return Point(left, top)
    return nearest_point


def callback_source(
    event: int,
    left: int,
    top: int,
    _flags: int,
    param: list[CalPoints | Counter],
) -> None:
    points: CalPoints = param[0]  # type: ignore[assignment]
    counter: Counter = param[1]  # type: ignore[assignment]
    if event == EVENT_LBUTTONDOWN and counter.source_click < 4:
        points.source_points.append(Point(left - BORDERSIZE, top - BORDERSIZE))
        counter.source_click += 1
    if (event in (EVENT_MBUTTONDOWN, EVENT_RBUTTONDOWN)) and counter.source_click:
        print("remove last point", points.source_points.pop())
        counter.source_click -= 1


def callback_target(
    event: int,
    left: int,
    top: int,
    _flags: int,
    param: list[CalPoints | Counter],
) -> None:
    points: CalPoints = param[0]  # type: ignore[assignment]
    counter: Counter = param[1]  # type: ignore[assignment]
    if event == EVENT_LBUTTONDOWN and counter.target_click < 4:
        points.target_points.append(find_nearest_point(left, top))
        counter.target_click += 1
    if (event in (EVENT_MBUTTONDOWN, EVENT_RBUTTONDOWN)) and counter.target_click:
        print("remove last point", points.target_points.pop())
        counter.target_click -= 1


def draw_image(
    name: str, image: Image, points: list[Point], had_border: bool = False
) -> None:
    for pid, point in enumerate(points):
        pointy = point.y
        pointx = point.x
        if had_border:
            pointy = pointy + BORDERSIZE
            pointx = pointx + BORDERSIZE
        image = draw_x(image, pointx, pointy, Color(0, 0, 0), line_width=3, size=50)
        image = add_text_to_image(
            image,
            str(pid),
            Point(pointx + 7, pointy - 10),
            font_scale=4,
            color=Color(0, 0, 255),
            thickness=7,
            line_type=LINE_AA,
        )
    imshow(name, image)


def move_crosshair(points: list[Point], key: int) -> None:
    inc = 1
    if len(points) == 0 or key == -1:
        return
    point = points[len(points) - 1]
    if key == ord("a"):
        point = Point(point.x - inc, point.y)
    if key == ord("d"):
        point = Point(point.x + inc, point.y)
    if key == ord("w"):
        point = Point(point.x, point.y - inc)
    if key == ord("s"):
        point = Point(point.x, point.y + inc)
    points[len(points) - 1] = point


def map_image(
    target_image: Image, points: CalPoints, counter: Counter, focal: int
) -> None:
    startWindowThread()

    namedWindow("source", WINDOW_NORMAL)
    namedWindow("target", WINDOW_NORMAL)
    setMouseCallback("source", callback_source, param=[points, counter])
    setMouseCallback("target", callback_target, param=[points, counter])

    transformation = Transformation(get_basic_transformer_combination_config())
    transformation.set_focal(focal)
    source_image = imread(FILE_PATH)
    if CAMERA_NAME[6] == "t":
        left, _right = split_image(source_image)
        source_image = left

    border_image = copyMakeBorder(
        source_image,
        top=BORDERSIZE,
        bottom=BORDERSIZE,
        left=BORDERSIZE,
        right=BORDERSIZE,
        borderType=BORDER_CONSTANT,
        value=[0, 0, 0],
    )
    transformed_image = transformation.focal.normalize_image(border_image)

    while True:
        draw_image(
            "source", copy(transformed_image), points.source_points, had_border=True
        )
        draw_image("target", copy(target_image), points.target_points)
        key = waitKey(50)
        if key in (27, 13):  # esc or enter
            break
        move_crosshair(points.source_points, key)

    counter.source_click = 0
    counter.target_click = 0
    destroyAllWindows()


def show_image(file_path: str, calpoints: CalPoints, focal: int) -> None:
    namedWindow("only warp", WINDOW_NORMAL)
    namedWindow("undistort and warp", WINDOW_NORMAL)

    transformation = Transformation(get_basic_transformer_combination_config())
    transformation.set_cal_points(calpoints)
    transformation.set_focal(focal)
    source_image = imread(file_path)

    only_warp = transformation.focal.normalize_image(source_image)
    imshow("only warp", only_warp)

    transformed = transformation.transform_image(source_image)
    imshow("undistort and warp", transformed)

    waitKey(0)


def cleanup_matrix(matrix_array: Matrix) -> str:
    matrix_string = str(matrix_array)
    matrix_string = matrix_string.replace("[", "")
    matrix_string = matrix_string.replace("]", "")
    matrix_string = matrix_string.replace("\n", "")
    return matrix_string


def get_target_image() -> Any:
    return imread("images/calibration.jpg")


def get_args() -> Any:
    parser = ArgumentParser(description="yolo")
    parser.add_argument(
        "-c",
        "--camera",
        type=str,
        required=True,
        help="camera name from config",
    )

    parser.add_argument(
        "-s",
        "--show",
        default=False,
        action="store_true",
        help="show the transformed image after calibration",
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config/sand_config.yaml",
        help="path to config file",
    )

    parser.add_argument(
        "--mapdefinition",
        type=str,
        default="config/terminal/woerth.yaml",
        help="path to map definition",
    )

    return parser.parse_args()


def get_calibration_test_points() -> CalPoints:
    point = CalPoints(
        target_points=[
            Point(1, 1),
            Point(1, 2),
            Point(2, 2),
            Point(2, 1),
        ],
        source_points=[
            Point(1, 1),
            Point(1, 2),
            Point(2, 2),
            Point(2, 1),
        ],
    )
    return point


def point_to_str(points: list[Point]) -> str:
    point_str = ""
    for point in points:
        point_str += f"({point.x},{point.y}),"
    return point_str[:-1].replace(",", ", ")


def main() -> None:
    global CAMERA_NAME, CAMERA_ID, FILE_PATH  # pylint: disable=global-statement
    args = get_args()
    config = get_config(args.config)

    target_image = get_target_image()
    CAMERA_NAME = args.camera
    CAMERA_ID = get_camera_id(config, CAMERA_NAME)
    FILE_PATH = get_path_from_camera_name(CAMERA_NAME).as_posix()
    source_image = imread(FILE_PATH)

    focal = config.cameras[CAMERA_ID].focal
    counter = Counter()

    with open(args.mapdefinition, encoding="utf-8") as map_definition_file:
        map_definition = yaml.load(map_definition_file, Loader=yaml.FullLoader)
    nullpoint_x = map_definition["nullpoint"]["horizontal"]
    nullpoint_y = map_definition["nullpoint"]["vertical"]

    for point_config in map_definition["calibration_points"]:
        point = Point(
            point_config["horizontal"] + nullpoint_x,
            point_config["vertical"] + nullpoint_y,
        )
        point_list.append(point)

    print(f"file_path: {FILE_PATH}")
    print(f"FILE DIMENSIONS: {imread(FILE_PATH).shape}")

    if CAMERA_ID < 0:
        print("no helper for camera found")
        sys.exit()

    cal_points = CalPoints(target_points=[], source_points=[])
    print(f"run map_image with camera {CAMERA_NAME}")
    print("")
    print("use Mouse to set calibration points in the Images")
    print("use WASD to move the last Point in source Image")
    print("on target Image the point will be automaticly the nearest crosshair")
    print("")
    map_image(target_image, cal_points, counter, focal)

    if args.show:
        show_image(FILE_PATH, cal_points, focal)

    destroyAllWindows()
    print()
    print("calibration data is not written to config file. Please do it yourself :-)")
    print()
    print(f'transformation_source_points: "[{point_to_str(cal_points.source_points)}]"')
    print(f'transformation_target_points: "[{point_to_str(cal_points.target_points)}]"')

    height, width = source_image.shape[:2]
    print(f"transformation_source_resolution_str: {width}x{height}")
    print()
    print()


if __name__ == "__main__":
    main()
