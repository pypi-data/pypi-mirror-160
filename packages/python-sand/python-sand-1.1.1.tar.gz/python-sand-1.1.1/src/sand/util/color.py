from __future__ import annotations

from sand.datatypes import Color

from .camera import get_level

camera_colors_by_level = {
    1: Color(150, 34, 150),
    2: Color(191, 122, 10),
    3: Color(4, 217, 171),
}
DEFAULT_COLOR = Color(0, 0, 0)


def get_color(camera_name: str) -> Color:
    level = get_level(camera_name)
    return camera_colors_by_level.get(level, DEFAULT_COLOR)


def get_lidar_color(lidar_name: str) -> Color:
    red = 0
    green = 255
    blue = int(lidar_name[1]) * 50
    if lidar_name[7] == "a":
        red = 255
    return Color(blue, green, red)
