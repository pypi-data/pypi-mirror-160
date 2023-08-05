from __future__ import annotations

from numpy import delete, hstack, unique, zeros

from sand.datatypes import LidarPoints


def remove_ground(data: LidarPoints, ground_level: float) -> LidarPoints:
    # we remove all values with z < 0
    data_filter = data[:, 2] > ground_level
    without_ground: LidarPoints = data[data_filter]
    return without_ground


def remove_over_max_level(data: LidarPoints, max_level: float) -> LidarPoints:
    # we remove all values with z < 0
    data_filter = data[:, 2] < max_level
    without_ground: LidarPoints = data[data_filter]
    return without_ground


def filter_duplicates(data: LidarPoints) -> LidarPoints:
    filtered: LidarPoints = unique(data, axis=0)
    return filtered


def flat(data: LidarPoints) -> LidarPoints:
    data = delete(data, [2], axis=1)
    zcolumn = zeros((len(data), 1))
    flattened: LidarPoints = hstack((data, zcolumn))
    return flattened


def filter_to_2d(points3d: LidarPoints) -> LidarPoints:
    points2d = remove_ground(points3d, 0.0)
    points2d = remove_over_max_level(points2d, 2.0)
    points2d = flat(points2d)
    return filter_duplicates(points2d)
