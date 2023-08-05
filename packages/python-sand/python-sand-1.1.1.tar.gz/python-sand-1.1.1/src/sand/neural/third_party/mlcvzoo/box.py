""" Class for Bounding Box information"""
from typing import NamedTuple


class Box(NamedTuple):
    """
    Class for storing bounding box information.

    Box on an Image:
    |-----------------------|
    |(xmin, ymin)           |
    |                       |
    |                       |
    |                       |
    |                       |
    |                       |
    |           (xmax, ymax)|
    |-----------------------|
    """

    xmin: int
    ymin: int
    xmax: int
    ymax: int
