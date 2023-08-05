from __future__ import annotations

import threading
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from cv2 import WINDOW_NORMAL, destroyAllWindows, imshow, namedWindow, waitKey

from sand.calibration.classes.map import CalibrationMap
from sand.calibration.classes.state import State
from sand.calibration.helper.calibration import calibration_points_from_id
from sand.config import SandConfig, change_to_playback_config, get_config
from sand.datatypes import CalPoints, LidarTransformation, Point
from sand.util.camera import get_level

SHUTDOWN = threading.Event()
ACTIVE_CAMERA_CHANGE = False

SAND_CONFIG: SandConfig
STATE: State
CALMAP: CalibrationMap


def transform_thread(camera_name: str) -> None:
    CALMAP.transform_image(camera_name)


def build_map() -> None:
    threads = []
    sleep_time = 0.001
    for _, value in enumerate(STATE.camera_names()):
        thread = threading.Thread(target=transform_thread, args=(value,))
        threads.append(thread)
        thread.start()
    for _, thread in enumerate(threads):
        thread.join()

    while not SHUTDOWN.is_set():
        CALMAP.reset_image_only_work_map()
        for name in sorted(STATE.camera_names(), reverse=True):
            if get_level(name) == 3:
                CALMAP.add_image_to_image_only_map(name)
                SHUTDOWN.wait(sleep_time)
        for name in sorted(STATE.camera_names(), reverse=True):
            if get_level(name) == 2:
                CALMAP.add_image_to_image_only_map(name)
                SHUTDOWN.wait(sleep_time)
        CALMAP.save_image_only_work_map()
        sleep_time = 0.5


def update_active_camera() -> None:
    global ACTIVE_CAMERA_CHANGE  # pylint: disable=global-statement
    while not SHUTDOWN.wait(0.1):
        if ACTIVE_CAMERA_CHANGE:
            ACTIVE_CAMERA_CHANGE = False
            CALMAP.draw_active_camera()


def enriche_map() -> None:
    while not SHUTDOWN.wait(0.05):
        CALMAP.enrich_map()


def lidar() -> None:
    CALMAP.state.read_lidars()
    while not SHUTDOWN.wait(0.1):
        CALMAP.draw_lidar_points()


def get_args() -> Any:
    parser = ArgumentParser(description="yolo")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="config/sand_config.yaml",
        help="path to config file",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default="",
        help="path to segment for lidar data",
    )
    parser.add_argument(
        "-m",
        "--nomap",
        default=False,
        action="store_true",
        help="don't show the generated map in the background",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=float,
        default=0.1,
        help="scale of map, default 0.1",
    )
    return parser.parse_args()


def init_system() -> tuple[Any, SandConfig]:
    args = get_args()
    config = get_config(args.config)
    return (args, config)


def get_calibration_points(camera_id: int) -> CalPoints:
    return calibration_points_from_id(SAND_CONFIG, camera_id)


def point_to_str(points: list[Point]) -> str:
    point_str = ""
    for point in points:
        point_str += f"({point.x},{point.y}),"
    return point_str[:-1].replace(",", ", ")


def lidar_transformation_to_str(trans: LidarTransformation) -> str:
    return f"[{trans.x}, {trans.y}, {trans.z}, {trans.angle}]"


def process_key(  # pylint: disable=too-many-branches, too-many-statements
    key: int,
) -> None:
    global ACTIVE_CAMERA_CHANGE  # pylint: disable=global-statement

    # LIDAR

    if key == ord("m"):
        STATE.next_lidar()
    if key == ord("."):
        STATE.prev_lidar()

    inc = 0.1
    if key == ord("j"):
        STATE.move_lidar(-inc, 0)
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("l"):
        STATE.move_lidar(inc, 0)
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("i"):
        STATE.move_lidar(0, -inc)
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("k"):
        STATE.move_lidar(0, inc)
        ACTIVE_CAMERA_CHANGE = True

    if key == ord("o"):
        STATE.rotate_lidar(-1.0)
    if key == ord("u"):
        STATE.rotate_lidar(1.0)

    # CAMERA
    if key == ord("1"):
        STATE.change_focal(+50)
    if key == ord("3"):
        STATE.change_focal(-50)

    if key == ord("e"):
        STATE.next_point()
    if key == ord("q"):
        STATE.prev_point()

    if key == ord("c"):
        STATE.next_camera()
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("y"):
        STATE.prev_camera()
        ACTIVE_CAMERA_CHANGE = True

    inc = 2
    if key == ord("a"):
        STATE.move_point(-inc, 0)
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("d"):
        STATE.move_point(inc, 0)
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("w"):
        STATE.move_point(0, -inc)
        ACTIVE_CAMERA_CHANGE = True
    if key == ord("s"):
        STATE.move_point(0, inc)
        ACTIVE_CAMERA_CHANGE = True

    # MISC

    if key == ord("p"):
        print()
        print(f'camera: "{CALMAP.state.active_cam.name}"')
        print(
            f'transformation_source_points: "[{point_to_str(CALMAP.state.active_cam.corner_calibration_points.source_points)}]"'
        )
        print(
            f'transformation_target_points: "[{point_to_str(CALMAP.state.active_cam.corner_calibration_points.target_points)}]"'
        )
        print(f'focal: "{CALMAP.state.active_cam.focal}"')
        print()
        print(
            f'lidar: "{CALMAP.state.lidar_list[CALMAP.state.active_lidar_index].config.name}"'
        )
        print(
            f'lidar_transformation: "{lidar_transformation_to_str(CALMAP.state.lidar_list[CALMAP.state.active_lidar_index].vlp_cloud.transformation)}"'
        )

    if key == ord("n"):
        CALMAP.toggle_show_map()
        print("show map", CALMAP.show_map)


def print_keybinding() -> None:
    print("w,a,s,d for moving point")
    print("u,i for changing active point")
    print("j,k for changing active camera")


def main() -> None:
    global CALMAP, STATE, SAND_CONFIG, ACTIVE_CAMERA_CHANGE  # pylint: disable=global-statement
    build_map_thread = threading.Thread(target=build_map, args=())
    active_camera_thread = threading.Thread(target=update_active_camera, args=())
    enrich_map_thread = threading.Thread(target=enriche_map, args=())
    lidar_thread = threading.Thread(target=lidar, args=())
    try:
        args, SAND_CONFIG = init_system()
        if args.path != "":
            SAND_CONFIG = change_to_playback_config(SAND_CONFIG, Path(args.path))
        STATE = State(SAND_CONFIG)
        CALMAP = CalibrationMap(STATE, args.scale)
        ACTIVE_CAMERA_CHANGE = True
        if args.nomap:
            CALMAP.show_map = False
        build_map_thread.start()
        enrich_map_thread.start()
        active_camera_thread.start()
        lidar_thread.start()

        namedWindow("map", WINDOW_NORMAL)

        while True:
            imshow("map", CALMAP.enriched_map)
            key = waitKey(50)
            if key in (27, 13):  # esc or enter
                break
            process_key(key)
    except KeyboardInterrupt:
        destroyAllWindows()
        SHUTDOWN.set()


if __name__ == "__main__":
    main()
