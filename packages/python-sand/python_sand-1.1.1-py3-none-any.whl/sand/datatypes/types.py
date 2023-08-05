from __future__ import annotations

from datetime import datetime
from typing import List, NamedTuple, Tuple

from nptyping import Float, Int, NDArray, Shape

CameraName = str
Matrix = NDArray[Shape["Height, Width"], Float]
Image = NDArray[Shape["Height, Width, 3 color"], Int]
Size = Tuple[int, int]


class Point(NamedTuple):
    x: int
    y: int


class Points(NamedTuple):
    source: Point
    target: Point


Polygon = List[Point]
CollisionMap = List[List[int]]
HeatMapArray = NDArray[Shape["Height, Width"], Float]


class LidarTransformation(NamedTuple):
    x: float
    y: float
    z: float
    angle: float


class LidarRawPoint(NamedTuple):
    distance: float
    angle: float
    row: int


LidarPoints = NDArray[Shape["Count, [x, y, z]"], Float]


class Box(NamedTuple):
    """
    A detection on a Frame, format::
        |-------|

        |[0]  [1]|

        |        |

        |[2]  [3]|

        |-------|
    """

    upper_right: Point
    upper_left: Point
    lower_left: Point
    lower_right: Point


class CalPoints(NamedTuple):
    source_points: list[Point]
    target_points: list[Point]


class Color(NamedTuple):
    blue: int
    green: int
    red: int


class Dimensions(NamedTuple):
    width: int
    height: int


class TaskTimestamp(NamedTuple):
    task: str
    time: datetime


Topic = str
