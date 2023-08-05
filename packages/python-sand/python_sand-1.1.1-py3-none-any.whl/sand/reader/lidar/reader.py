from __future__ import annotations

from socket import AF_INET, SOCK_DGRAM, socket

from overrides import overrides

from sand.config import LidarConfig
from sand.logger import Logger


class LidarDeviceReader:
    def __init__(self, config: LidarConfig, log: Logger) -> None:
        self.config = config
        self.log = log

    def get_packet(self) -> bytes:
        pass

    def close(self) -> None:
        pass


class LidarFileReader(LidarDeviceReader):
    def __init__(self, config: LidarConfig, log: Logger) -> None:
        LidarDeviceReader.__init__(self, config, log)

        self.file = open(  # pylint: disable=consider-using-with
            self.config.file_path, "rb"
        )

    def get_packet(self) -> bytes:
        data = self.file.read(1210)
        if data[1206:] == b"DUDE":
            return data[:1206]
        self.log.w(
            "a wild file end appeared - no more lidar data in file", "get_packet"
        )
        self.file.seek(0)
        self.log.d("resetted file pointer to 0", "get_packet")
        return b""

    @overrides
    def close(self) -> None:
        self.file.close()


class Vlp16Reader(LidarDeviceReader):
    def __init__(self, config: LidarConfig, log: Logger) -> None:
        LidarDeviceReader.__init__(self, config, log)

        self.soc = socket(AF_INET, SOCK_DGRAM)
        self.soc.bind(("", self.config.data_port))
        self.soc.settimeout(1)

    def get_packet(self) -> bytes:
        return self.soc.recv(1206)

    @overrides
    def close(self) -> None:
        self.soc.close()
