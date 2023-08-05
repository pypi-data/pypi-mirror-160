from __future__ import annotations

from datetime import datetime
from struct import unpack_from
from typing import Any

from sand.util.time import now

from .types import LidarPoints, TaskTimestamp


class LidarPacket:
    def __init__(self, lidar_name: str, packet: bytes):
        self.lidar_name: str = lidar_name
        assert (
            len(packet) == 1206
        ), f"packet data is not 1206 byte long, is: {len(packet)}"
        self.packet = packet  # 1206 bytes long
        self.timestamp = LidarPacket._get_timestamp(self.timestamp_in_bytes)

    @property
    def data(self) -> bytes:
        # packet is 1200 bytes long
        return self.packet[:1200]

    @property
    def timestamp_in_bytes(self) -> bytes:
        # timestamp is 6 bytes long with an offset of 1200 bytes
        return self.packet[1200:]

    @staticmethod
    def _get_timestamp(data: bytes) -> datetime:
        timestamp_and_factory: tuple[float, Any] = unpack_from("<IH", data)  # type: ignore[assignment]
        timestamp, _factory = timestamp_and_factory
        return datetime.utcfromtimestamp(timestamp)

    def __str__(self) -> str:
        return (
            f"LidarPacket: {{ lidar_name: {self.lidar_name}, timestamp: {self.timestamp}, "
            f"timestamp array: {self.timestamp_in_bytes.hex()}}}"
        )


class EnrichedLidarPacket:
    def __init__(
        self, timestamp: datetime, points: LidarPoints, points2d: LidarPoints
    ) -> None:
        self.points = points
        self.points2d = points2d
        self.timestamp = timestamp  # creation time
        self.timestamps: list[TaskTimestamp] = []

    def add_timestamp(self, name: str) -> None:
        self.timestamps.append(TaskTimestamp(name, now()))
