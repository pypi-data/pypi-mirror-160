from __future__ import annotations

from sand.config import SandConfig


def camera_name_list(config: SandConfig) -> list[str]:
    cam_names = []
    for camera_config in config.cameras:
        cam_names.append(camera_config.name)
    return cam_names
