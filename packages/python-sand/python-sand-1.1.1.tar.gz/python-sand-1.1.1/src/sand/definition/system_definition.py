from __future__ import annotations

from functools import partial
from math import ceil
from pathlib import Path
from typing import cast

import prctl
from config_builder import ConfigBuilder

from sand.config import (
    CameraConfig,
    ConstantConfig,
    SandConfig,
    change_to_playback_config,
)
from sand.config.helpers import (
    is_box_transformer_active,
    is_camera_isolated,
    is_camera_writer_active,
    is_converter_active,
    is_drive_watcher_active,
    is_fusion_active,
    is_image_transformer_active,
    is_lidar_active,
    is_lidar_packet_enricher_active,
    is_lidar_writer_active,
    is_map_active,
    is_metric_active,
    is_neural_active,
    is_publisher_active,
)
from sand.datatypes import Dimensions
from sand.interfaces.synchronization import Isolator
from sand.logger import Logger
from sand.reader.video import CameraSystem  # allowed
from sand.util.config_publisher import publish_config
from sand.view.stream.pipeline.stream_server import StreamServer  # allowed

# pylint: disable=import-outside-toplevel


def _is_primary_system(gpu_index: int, gpus: int) -> bool:
    return gpus == -1 or gpu_index == 0


def _start_camera_system(
    camera_config: CameraConfig, sand_config: SandConfig, is_playback: bool
) -> CameraSystem:
    log = Logger("camera system")
    camera_system = CameraSystem(camera_config, sand_config, is_playback)
    log.d("camera system is up", camera_config.name)
    if is_camera_writer_active(camera_config):
        from sand.recorder.video.pipeline.recorder import CameraRecorder

        CameraRecorder(camera_system, sand_config.communication, is_playback)
        log.d("camera recorder is up", camera_config.name)

    camera_system.start()
    return camera_system


def _start_debug_system(sand_config: SandConfig, is_playback: bool) -> None:
    log = Logger("debug system")

    log.d("Building debug system", "_start_debug_system")
    for camera_config in sand_config.cameras:
        if is_image_transformer_active(sand_config):
            from sand.reader.video import FrameDecoder

            decoder = FrameDecoder(camera_config, sand_config.communication)
            from sand.transformer.pipeline.image import ImageTransformer

            ImageTransformer(decoder, camera_config.name, sand_config, is_playback)

    log.d("Decoder and transformer are up", "_start_debug_system")

    # start after Transformer
    # depents on boxtransformer, Imagetransformer, Fusion, LidarPacketEnricher
    if is_map_active(sand_config):
        from sand.map import MapBuilder, MapEnricher

        dimension = Dimensions(
            sand_config.map_builder.map_width, sand_config.map_builder.map_height
        )

        builder = MapBuilder(sand_config, is_playback)
        enricher = MapEnricher(sand_config, is_playback, builder)
        StreamServer(
            "map_builder",
            7999,
            dimension,
            sand_config.communication,
            builder,
        )
        StreamServer(
            "map_enricher",
            7998,
            dimension,
            sand_config.communication,
            enricher,
        )
        if sand_config.map_builder.record:
            from sand.recorder.map.pipeline.map_recorder import MapRecorder

            MapRecorder(sand_config, enricher)
        log.d("MapBuilder is up", "_start_debug_system")


def _start_publisher(sand_config: SandConfig) -> None:
    log = Logger("debug system")

    # start after all CollectAbles
    if is_publisher_active(sand_config):
        from sand.view.frontend import Publisher

        Publisher(sand_config)

    log.d("Publisher is up", "_start_debug_system")
    prctl.set_proctitle("SAND_publisher")


def _get_camera_group(
    camera_configs: list[CameraConfig], gpus: int, gpu_index: int
) -> range:
    camera_count = len(camera_configs)
    indices = range(camera_count)

    if gpus < 2:
        # only one gpu or no multi -> one big group
        return indices

    chunk_size = ceil(camera_count / gpus)
    chunks = [
        indices[index : index + chunk_size]
        for index in range(0, camera_count, chunk_size)
    ]
    return chunks[gpu_index]


def _start_multi_gpu_camera_system(
    sand_config: SandConfig,
    is_playback: bool,
    gpu_index: int,
    gpus: int,
) -> None:
    log = Logger("multi gpu camera starter")

    camera_indices = _get_camera_group(sand_config.cameras, gpus, gpu_index)

    camera_systems: list[CameraSystem] = []
    for camera_index in camera_indices:
        camera_config = sand_config.cameras[camera_index]
        if is_camera_isolated(sand_config):
            Isolator(
                target=partial(
                    _start_camera_system,
                    camera_config=camera_config,
                    sand_config=sand_config,
                    is_playback=is_playback,
                ),
                global_config=sand_config,
                name=f"b_{camera_config.name}",
            )
        else:
            camera_systems.append(
                _start_camera_system(
                    camera_config=camera_config,
                    sand_config=sand_config,
                    is_playback=is_playback,
                )
            )
        if is_box_transformer_active(sand_config):
            from sand.transformer.pipeline.box import BoxTransformer

            Isolator(
                target=partial(
                    BoxTransformer,
                    camera_name=camera_config.name,
                    global_config=sand_config,
                    playback=is_playback,
                ),
                global_config=sand_config,
                name=f"b_{camera_config.name}",
            )
    if is_neural_active(sand_config):
        from sand.neural.pipeline.neural import NeuralNetwork

        NeuralNetwork(camera_systems, sand_config)
        log.d("neural net is up", "_start_multi_gpu_camera_system")


def _start_lidar(sand_config: SandConfig, is_playback: bool) -> None:
    for lidar_config in sand_config.lidars:
        if is_lidar_active(lidar_config):
            from sand.reader.lidar import LidarSystem

            lidar = LidarSystem(lidar_config, is_playback, sand_config)
            if is_lidar_writer_active(lidar_config):
                from sand.recorder.lidar.pipeline.recorder import LidarRecorder

                LidarRecorder(
                    lidar, lidar_config, sand_config.communication, is_playback
                )
    if is_lidar_packet_enricher_active(sand_config):
        from sand.reader.lidar import LidarPacketEnricher

        LidarPacketEnricher(sand_config)


def start_primary_system(sand_config: SandConfig, is_playback: bool) -> None:
    Isolator(
        target=lambda: _start_lidar(sand_config, is_playback),
        global_config=sand_config,
        name="lidar",
    )
    Isolator(
        target=lambda: _start_debug_system(sand_config, is_playback),
        global_config=sand_config,
        name="debug_system",
    )
    Isolator(
        target=lambda: _start_publisher(sand_config),
        global_config=sand_config,
        name="publisher",
    )
    # start after DriverWatcher
    if is_converter_active(sand_config):
        from sand.converter import Converter

        Isolator(
            target=lambda: Converter(sand_config),
            global_config=sand_config,
            name=Converter.__name__,
        )
    if is_metric_active(sand_config):
        from sand.metric.committer import Committer
        from sand.metric.delta import DeltaCollector

        Isolator(
            target=partial(DeltaCollector, global_config=sand_config),
            global_config=sand_config,
            name=DeltaCollector.__name__,
        )
        Isolator(
            target=lambda: Committer(sand_config),
            global_config=sand_config,
            name=Committer.__name__,
        )
    # start after lidar and camera
    if is_fusion_active(sand_config):
        from sand.sensor_fusion import SensorFusion

        Isolator(
            target=lambda: SensorFusion(sand_config),
            global_config=sand_config,
            name=SensorFusion.__name__,
        )


def define_system(
    config: Path,
    playback_path: Path | None,
    gpu_index: int = -1,
    gpus: int = -1,
) -> None:
    fct = "start"
    log = Logger(f"system[{gpu_index=}]")
    is_playback = playback_path is not None

    log.i(f"{config=} | {playback_path=} | {gpus=} | {gpu_index=}", fct)

    ConstantConfig()
    config_builder = ConfigBuilder(
        class_type=SandConfig, yaml_config_path=config.as_posix()
    )
    sand_config = cast(SandConfig, config_builder.configuration)

    if is_playback:
        sand_config = change_to_playback_config(sand_config, playback_path)  # type: ignore[arg-type]

    if _is_primary_system(gpu_index, gpus):
        publish_config(sand_config)
        log.i("Configuration published to mqtt", fct)

    log.d(
        f"""sand_config.cameras: {', '.join(map(str, sand_config.cameras))}
sand_config.lidars: {', '.join(map(str, sand_config.lidars))}
{sand_config.publisher=}
{sand_config.watcher=}
{sand_config.metric=}
{sand_config.converter=}
{sand_config.neural=}
{sand_config.transformer=}
{sand_config.map_builder=}
Starting nodes...
        """,
        fct,
    )

    if _is_primary_system(gpu_index, gpus) and is_drive_watcher_active(sand_config):
        from sand.watcher import DriveWatcher

        Isolator(
            target=lambda: DriveWatcher(sand_config),
            global_config=sand_config,
            name=DriveWatcher.__name__,
        )

    _start_multi_gpu_camera_system(sand_config, is_playback, gpu_index, gpus)

    if _is_primary_system(gpu_index, gpus):
        start_primary_system(sand_config, is_playback)

    log.i("Finished startup", fct)

    prctl.set_proctitle(f"SAND_Main[{gpu_index=}]")
