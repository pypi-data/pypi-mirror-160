from __future__ import annotations

from math import cos, pi, sin
from struct import unpack_from
from typing import Any

from numpy import array, float64

from sand.datatypes import LidarPacket, LidarPoints, LidarTransformation
from sand.datatypes.types import LidarRawPoint


def _get_angle(data: bytes, offset: int) -> int:
    flag_and_angle: tuple[Any, int] = unpack_from("<HH", data, offset)  # type: ignore[assignment]
    _flag, angle = flag_and_angle
    return angle


def _get_slice(data: bytes, offset: int, step: int) -> bytes:
    data_slice: bytes = unpack_from("<" + "HB" * 16, data, offset + 4 + step * 48)  # type: ignore[assignment]
    return data_slice


def _calc_offset(sequence: int, row: int) -> float:
    return (
        Vlp16Cloud.time_between_two_slices * sequence
        + Vlp16Cloud.time_between_two_laser_flashes * row
    ) / Vlp16Cloud.from_microseconds_to_seconds


class Vlp16Cloud:
    time_between_two_slices = 55.296
    time_between_two_laser_flashes = 2.304
    from_microseconds_to_seconds = 1000000.0
    _distance_resolution = 0.002
    _slices_per_360 = 360
    _rows = 16
    _angles = [-15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]

    def __init__(self, lidar_name: str, transformation: LidarTransformation) -> None:
        self._lidar_name = lidar_name
        self.transformation = transformation
        self.cloud: LidarPoints = array(
            [[0.0, 0.0, 0.0]] * self._rows * self._slices_per_360, dtype=float64
        )
        self.cloud_raw: list[LidarRawPoint] = []
        for _ in range(self._rows * self._slices_per_360):
            self.cloud_raw.append(LidarRawPoint(distance=0.0, angle=0.0, row=0))

    def set_transformation(self, transformation: LidarTransformation) -> None:
        self.transformation = transformation
        self._recalc_cloud()

    def _recalc_cloud(self) -> None:
        for raw in self.cloud_raw:
            self._calc_point(raw.distance, raw.angle, raw.row)

    def _calc_point(
        self,
        distance: float,
        angle: float,
        row: int,
    ) -> None:
        radius = distance * self._distance_resolution
        alpha = ((angle / 100.0) + self.transformation.angle) * pi / 180.0
        omega = self._angles[row] * pi / 180.0
        rad_omega = radius * cos(omega)
        value_x = round(rad_omega * sin(alpha), 1) + self.transformation.x
        value_y = -1 * round(rad_omega * cos(alpha), 1) + self.transformation.y
        value_z = round(radius * sin(omega), 1) + self.transformation.z
        point_number = int(angle / 100) * self._rows + row
        self.cloud[point_number] = [value_x, value_y, value_z]
        self.cloud_raw[point_number] = LidarRawPoint(
            distance=distance, angle=angle, row=row
        )

    def get_cloud(self) -> LidarPoints:
        return self.cloud

    def update_point_cloud(self, packet: LidarPacket) -> None:
        data = packet.packet
        offset = 0
        while offset < 1200:
            angle = _get_angle(data, offset)
            for step in range(2):
                vlp_slice = _get_slice(data, offset, step)
                for row in range(self._rows):
                    self._calc_point(vlp_slice[row * 2], angle, row)
            offset += 100
