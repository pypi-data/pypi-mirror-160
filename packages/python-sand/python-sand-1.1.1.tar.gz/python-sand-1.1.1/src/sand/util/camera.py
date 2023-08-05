from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

_is_sand_sensor_name_pattern = re.compile(r"f(\d)_l(\d)_([vt]\d+|(li|la))")
_is_sand_thermal_camera_pattern = re.compile(r"f\d_l\d_t\d")
_is_sand_visual_camera_pattern = re.compile(r"f\d_l\d_v\d")


@lru_cache
def is_sand_camera_name(camera_name: str) -> bool:
    return _is_sand_sensor_name_pattern.match(camera_name) is not None


@lru_cache
def is_sand_thermal_camera(camera_name: str) -> bool:
    return _is_sand_thermal_camera_pattern.match(camera_name) is not None


@lru_cache
def is_sand_visual_camera(camera_name: str) -> bool:
    return _is_sand_visual_camera_pattern.match(camera_name) is not None


@lru_cache
def get_level(sensor_name: str) -> int:
    match = _is_sand_sensor_name_pattern.match(sensor_name)
    if match is not None:
        return int(match.group(2))
    return 1


@lru_cache
def get_foot(sensor_name: str) -> int:
    match = _is_sand_sensor_name_pattern.match(sensor_name)
    if match is not None:
        return int(match.group(1))
    return 1


@lru_cache
def get_number(sensor_name: str) -> int:
    match = _is_sand_sensor_name_pattern.match(sensor_name)
    if match is not None:
        sensor = match.group(3)

        if sensor[0] == "l":
            # we only have one lidar
            return 1

        return int(sensor[1])

    return 1


@lru_cache
def get_camera_name(file: str, default: str = "") -> str:
    matches = re.match(r".*(f\d_l\d_[tv]\d).*", file)
    if matches is None:
        return default
    return matches.groups()[0]


@lru_cache
def get_path_from_camera_name(
    name: str,
    file_ending: str = "jpg",
    folder: Path = Path("images/cameras"),
) -> Path:
    return folder.joinpath(name).with_suffix(f".{file_ending}")
