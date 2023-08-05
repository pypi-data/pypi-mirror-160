from __future__ import annotations

from pathlib import Path

from sand.config import SandConfig
from sand.reader.lidar import LidarSystem  # allowed


def get_packets(file_path: Path, lidar_name: str, number: int) -> list[bytes]:
    if file_path == "":
        return []
    possible_files = list(file_path.joinpath(lidar_name).glob("*f1_l1_la.velo"))
    if len(possible_files) == 1:
        with open(possible_files[0], "rb") as file:
            packets: list[bytes] = []
            for _ in range(number):
                data = file.read(1210)
                if data[1206:] == b"DUDE":
                    packets.append(data[:1206])
            return packets
    return []


def init_lidar(config: SandConfig) -> list[LidarSystem]:
    lidar_systems: list[LidarSystem] = []
    for lidar_config in config.lidars:
        lidar_systems.append(
            LidarSystem(lidar_config, is_playback=True, sand_config=config)
        )
    return lidar_systems


def shutdown_lidar(lidar_systems: list[LidarSystem]) -> None:
    for lidar in lidar_systems:
        lidar.reader.shutdown()
        lidar.collector.shutdown()
