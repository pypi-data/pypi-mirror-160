from __future__ import annotations

from sand.config.config import LidarConfig
from sand.datatypes import LidarPacket, LidarPoints
from sand.reader.lidar.cloud import Vlp16Cloud  # allowed
from sand.util.lidar import filter_to_2d


class Lidar:
    cloud2d: LidarPoints
    cloud3d: LidarPoints

    def __init__(self, config: LidarConfig):
        self.config = config
        self.vlp_cloud = Vlp16Cloud(config.name, self.config.transformation)

    def _get_packet(self) -> bytes:
        data: bytes = self.file.read(1210)
        if data[1206:] == b"DUDE":
            return data[:1206]
        print(
            "[Lidar] a wild file end appeared - no more lidar data in file",
            "get_packet",
        )
        self.file.seek(0)
        print("[Lidar] resetted file pointer to 0")
        return b""

    def read_cloud(self) -> None:
        if self.config.file_path != "":
            self.file = open(  # pylint: disable=consider-using-with, attribute-defined-outside-init)
                self.config.file_path, "rb"
            )
            for _ in range(100):
                data = self._get_packet()
                packet = LidarPacket(self.config.name, data)
                self.vlp_cloud.update_point_cloud(packet)
            print("[Lidar] read done ", self.config.name)
        else:
            print("[Lidar] no lidar file for", self.config.name)

    def get_cloud(self) -> LidarPoints:
        return self.vlp_cloud.get_cloud()

    def get_2d_cloud(self) -> LidarPoints:
        return filter_to_2d(self.vlp_cloud.get_cloud())
