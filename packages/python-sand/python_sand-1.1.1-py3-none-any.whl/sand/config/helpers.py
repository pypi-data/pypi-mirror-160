from __future__ import annotations

from .config import CameraConfig, LidarConfig, SandConfig


def is_box_transformer_active(sand_config: SandConfig) -> bool:
    return sand_config.neural.active and (
        sand_config.map_builder.active or sand_config.sensor_fusion.active
    )


def is_camera_writer_active(camera_config: CameraConfig) -> bool:
    return camera_config.writer_active


def is_neural_active(sand_config: SandConfig) -> bool:
    return sand_config.neural.active


def is_image_transformer_active(sand_config: SandConfig) -> bool:
    return sand_config.transformer.active


def is_lidar_active(lidar_config: LidarConfig) -> bool:
    return lidar_config.active


def is_lidar_writer_active(lidar_config: LidarConfig) -> bool:
    return lidar_config.writer_active


def is_lidar_packet_enricher_active(sand_config: SandConfig) -> bool:
    return (
        any(map(lambda c: c.active, sand_config.lidars))
        and sand_config.lidar_enricher.active
    )


def is_fusion_active(sand_config: SandConfig) -> bool:
    return sand_config.sensor_fusion.active and (
        is_lidar_packet_enricher_active(sand_config)
        or is_box_transformer_active(sand_config)
    )


def is_map_active(sand_config: SandConfig) -> bool:
    return sand_config.map_builder.active and (
        is_box_transformer_active(sand_config)
        or is_image_transformer_active(sand_config)
        or is_fusion_active(sand_config)
        or is_lidar_packet_enricher_active(sand_config)
    )


def is_converter_active(sand_config: SandConfig) -> bool:
    return sand_config.converter.active


def is_metric_active(sand_config: SandConfig) -> bool:
    return sand_config.metric.active


def is_drive_watcher_active(sand_config: SandConfig) -> bool:
    return any(map(lambda c: c.writer_active, sand_config.lidars)) or any(
        map(lambda c: c.writer_active, sand_config.cameras)
    )


def is_publisher_active(sand_config: SandConfig) -> bool:
    return sand_config.publisher.active


def is_camera_isolated(sand_config: SandConfig) -> bool:
    return not is_neural_active(sand_config)
