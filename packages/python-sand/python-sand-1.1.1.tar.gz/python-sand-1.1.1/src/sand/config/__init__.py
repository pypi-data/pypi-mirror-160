"""Module for our configuration

It provides different configuration classes for the other modules. Generally the configuration class is named like the
module or the specific class for which the configuration is needed.
"""
from typing import cast

from config_builder import ConfigBuilder

from .config import *
from .transformer_combination_config import TransformerCombinationConfig


def get_config(config_path: str) -> SandConfig:
    ConstantConfig()
    config_builder = ConfigBuilder(class_type=SandConfig, yaml_config_path=config_path)
    return cast(SandConfig, config_builder.configuration)


def get_basic_transformer_combination_config() -> TransformerCombinationConfig:
    camera = CameraConfig()
    camera.stream_resolution_str = "2560x1440"
    camera.transformation_source_resolution_str = "2560x1440"
    transformer = TransformerConfig()
    return TransformerCombinationConfig(camera=camera, transformer=transformer)


def get_camera_id(sand_config: SandConfig, name: str) -> int:
    for cam_id, value in enumerate(sand_config.cameras):
        if value.name == name:
            return cam_id
    return -1
