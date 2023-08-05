from __future__ import annotations

import re
from argparse import ArgumentParser

import yaml
from cv2 import WINDOW_NORMAL, imread, imshow, imwrite, line, namedWindow, waitKey
from numpy import uint8, zeros

from sand.datatypes import Color, Point
from sand.util.image import draw_horizontal_line, draw_vertical_line, draw_x

IMAGE = zeros((1, 1, 3), uint8)


def mm_to_pixel(millimeter: int, pixel_per_meter: int = 100) -> int:
    return int(pixel_per_meter * millimeter / 1000)


def main() -> None:  # pylint: disable=too-many-locals
    parser = ArgumentParser(description="yolo")
    parser.add_argument(
        "-ppm", "--pixelpermeter", type=int, default=100, help="pixel per meter"
    )
    parser.add_argument(
        "-f", "--file", type=str, default="images/calibration.jpg", help="filename"
    )
    parser.add_argument(
        "-d",
        "--defintion",
        type=str,
        required=True,
        help="path to the map definition",
    )
    parser.add_argument(
        "-s",
        "--show",
        default=False,
        action="store_true",
        help="show generated IMAGE",
    )
    parser.add_argument(
        "-m",
        "--middlelines",
        default=False,
        action="store_true",
        help="generate middle lines",
    )

    parser.add_argument(
        "-g",
        "--gmaps",
        default=False,
        action="store_true",
        help="use gmaps as background",
    )

    args = parser.parse_args()
    with open(args.config, encoding="utf-8") as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    map_size_x = config["map"]["horizontal"]
    map_size_y = config["map"]["vertical"]
    nullpoint_x = config["nullpoint"]["horizontal"]
    nullpoint_y = config["nullpoint"]["vertical"]

    filename = args.file

    print("generation with config file:", args.config)
    print("horizontal map size:        ", map_size_x)
    print("vertical map size:          ", map_size_y)

    image = zeros((map_size_y, map_size_x, 3), uint8)
    image[:] = (255, 255, 255)
    if args.gmaps:
        image = imread("images/gmaps.png")

    line_width = 5
    color_lines = Color(50, 50, 50)
    color_nullpoint_lines = Color(255, 200, 255)
    color_points = Color(0, 0, 255)

    # Mittellinien
    if args.middlelines:
        image = draw_horizontal_line(image, nullpoint_y, color_nullpoint_lines)
        image = draw_vertical_line(image, nullpoint_x, color_nullpoint_lines)

    for line_str in config["lines"]:
        line_list = list(
            map(
                lambda match: (
                    int(float(match.split(",")[0])),
                    int(float(match.split(",")[1])),
                ),
                re.findall(
                    r"\(([-]?[0-9]*[.]?[0-9]*,[-]?[0-9]*[.]?[0-9]*)\)", line_str
                ),
            )
        )
        image = line(
            image,
            (line_list[0][0] + nullpoint_x, line_list[0][1] + nullpoint_y),
            (line_list[1][0] + nullpoint_x, line_list[1][1] + nullpoint_y),
            color_lines,
            line_width,
        )

    point_list = []
    for point_config in config["calibration_points"]:
        point = Point(
            point_config["horizontal"] + nullpoint_x,
            point_config["vertical"] + nullpoint_y,
        )
        point_list.append(point)
        image = draw_x(image, point.x, point.y, color_points, size=50, line_width=10)
        print(point)

    for rect in config["rectangulars"]:
        image = line(
            image,
            (rect["horizontal"] + nullpoint_x, rect["vertical"] + nullpoint_y),
            (
                rect["horizontal"] + nullpoint_x,
                rect["vertical"] + rect["height"] + nullpoint_y,
            ),
            color_lines,
            line_width,
        )
        image = line(
            image,
            (
                rect["horizontal"] + nullpoint_x,
                rect["vertical"] + rect["height"] + nullpoint_y,
            ),
            (
                rect["horizontal"] + rect["width"] + nullpoint_x,
                rect["vertical"] + rect["height"] + nullpoint_y,
            ),
            color_lines,
            line_width,
        )
        image = line(
            image,
            (rect["horizontal"] + nullpoint_x, rect["vertical"] + nullpoint_y),
            (
                rect["horizontal"] + rect["width"] + nullpoint_x,
                rect["vertical"] + nullpoint_y,
            ),
            color_lines,
            line_width,
        )
        image = line(
            image,
            (
                rect["horizontal"] + rect["width"] + nullpoint_x,
                rect["vertical"] + nullpoint_y,
            ),
            (
                rect["horizontal"] + rect["width"] + nullpoint_x,
                rect["vertical"] + rect["height"] + nullpoint_y,
            ),
            color_lines,
            line_width,
        )

    if args.show:
        window_name = "asd"
        namedWindow(window_name, WINDOW_NORMAL)
        imshow(window_name, image)
        waitKey(0)

    print("write to file: ", filename)
    imwrite(filename, image)


if __name__ == "__main__":
    main()
