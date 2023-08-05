from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

from cv2 import WINDOW_NORMAL, destroyAllWindows, imread, imshow, namedWindow, waitKey

from sand.config import (
    get_basic_transformer_combination_config,
    get_camera_id,
    get_config,
)
from sand.transformer.transformation import Transformation  # allowed
from sand.util.camera import get_path_from_camera_name, is_sand_thermal_camera
from sand.util.image import add_text_to_image, split_image

HELP_TEXT = """h -> toggle this help
s -> decrease focal by 100
w -> increase focal by 100
q -> exit"""


def find_focal(
    old_focal: int, camera_name: str, camera_id: int, file_path: Path
) -> int:
    print(f"Run focal | {camera_id=} | {camera_name=} | {old_focal=} | {file_path=}")

    focal = old_focal
    image = imread(str(file_path))
    print(f"{image.shape=}")
    if is_sand_thermal_camera(camera_name):
        left, _right = split_image(image)
        image = left

    show_help = True
    while True:
        transformation = Transformation(get_basic_transformer_combination_config())
        transformation.set_focal(focal)
        transformed_image = transformation.focal.normalize_image(image)
        output = (
            add_text_to_image(transformed_image, text=HELP_TEXT)
            if show_help
            else transformed_image
        )

        imshow("focal", output)

        key = waitKey(50)
        if key == ord("h"):
            show_help = not show_help
        elif key == ord("s"):
            focal = focal - 100
            print(focal)
        elif key == ord("w"):
            focal = focal + 100
            print(focal)
        elif key in (27, ord("q")):  # esc
            return focal


def main() -> None:
    parser = ArgumentParser(description="yolo")

    parser.add_argument(
        "-c",
        "--camera",
        type=str,
        required=True,
        help="camera name from config",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/sand_config.yaml",
        help="path to config file",
    )

    args = parser.parse_args()
    config = get_config(args.config)

    camera_name = args.camera
    camera_id = get_camera_id(config, camera_name)
    file_path = get_path_from_camera_name(camera_name)
    focal = int(config.cameras[camera_id].focal)
    namedWindow("focal", WINDOW_NORMAL)

    if camera_id < 0:
        print("no helper for camera found")
        sys.exit(3)

    new_focal = find_focal(focal, camera_name, camera_id, file_path)
    print(f"found focal {new_focal} for {camera_name}")
    print("write it manually in the config!")
    destroyAllWindows()


if __name__ == "__main__":
    main()
