from __future__ import annotations

from ast import literal_eval
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from re import search
from typing import DefaultDict, List, Tuple
from xml.dom import minidom

import related
from config_builder import BaseConfigClass

try:
    from mlcvzoo_base.configuration.model_config import ModelConfig
except ModuleNotFoundError:
    ModelConfig = BaseConfigClass  # type: ignore[assignment, misc]

from sand.datatypes import CalPoints, CameraName, Dimensions, LidarTransformation, Point
from sand.logger import Logger
from sand.registry import RegisterAble, get_singleton_node
from sand.util.camera import get_camera_name

log = Logger("config")


def _to_points(point_tuples: list[tuple[int, int]]) -> list[Point]:
    return list(map(lambda point_tuple: Point(*point_tuple), point_tuples))


@related.mutable(strict=True)
class CommunicationConfig(BaseConfigClass):
    # localhost not possible because of CI and docker defaulting to ipv6 and failing there
    host: str = related.StringField(default="127.0.0.1")
    use_mqtt: bool = related.BooleanField(default=True)


@related.mutable(strict=True)
class CameraConfig(BaseConfigClass):
    writer_active: bool = related.BooleanField(default=False)
    fps: int = related.IntegerField(default=25)
    name: str = related.StringField(default="webcam")
    stream: str = related.StringField(default="0")
    focal: int = related.IntegerField(default=1500)

    metric_interval: int = related.IntegerField(default=10)
    interesting_source: str = related.StringField(default="neural")  # movement, neural
    interesting_mode: str = related.StringField(default="off")  # off, single, all
    is_interesting_before: int = related.IntegerField(default=30)
    is_interesting_after: int = related.IntegerField(default=30)
    stream_resolution_str: str = related.StringField(default="2560x1440")
    transformation_source_resolution_str: str = related.StringField(default="3840x2160")
    serve_stream: bool = related.BooleanField(default=False)
    serve_port: int = related.IntegerField(default=-1)
    serve_boxes: bool = related.BooleanField(default=False)

    transformation_source_points: str = related.StringField(
        default="[(1, 1), (1, 2), (2, 2), (2, 1)]"
    )
    transformation_target_points: str = related.StringField(
        default="[(1, 1), (1, 2), (2, 2), (2, 1)]"
    )

    @property
    def stream_resolution(self) -> Dimensions:
        return CameraConfig.__get_resolution(self.stream_resolution_str)

    @property
    def transformation_source_resolution(self) -> Dimensions:
        return CameraConfig.__get_resolution(self.transformation_source_resolution_str)

    @staticmethod
    def __get_resolution(resolution_str: str) -> Dimensions:
        splitted = resolution_str.split("x")
        return Dimensions(int(splitted[0]), int(splitted[1]))

    @property
    def transformation(self) -> CalPoints:
        return self.__get_calibration_points(
            self.transformation_source_points,
            self.transformation_target_points,
        )

    def __get_calibration_points(
        self, source_points: str, target_points: str
    ) -> CalPoints:
        scaled_points: list[Point] = []
        for point in _to_points(literal_eval(source_points)):
            scaled_points.append(
                Point(
                    int(
                        point.x
                        / self.transformation_source_resolution.width
                        * self.stream_resolution.width
                    ),
                    int(
                        point.y
                        / self.transformation_source_resolution.height
                        * self.stream_resolution.height
                    ),
                )
            )
        return CalPoints(
            source_points=scaled_points,
            target_points=_to_points(literal_eval(target_points)),
        )


@related.mutable(strict=True)
class FrameStatsConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    process_delay: int = related.IntegerField(default=2)


@related.mutable(strict=True)
class CraneMapStatsConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)


@related.mutable(strict=False)
class NeuralNetworkConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    demo: bool = related.BooleanField(default=True)
    log_detections: bool = related.BooleanField(default=False)
    replacement_config_path: str | None = related.ChildField(
        cls=str, required=False, default=None
    )
    model_config: ModelConfig | None = related.ChildField(
        cls=ModelConfig,
        required=False,
        default=None,
    )
    wait_time_no_image_available: float = related.FloatField(default=0.2)


@related.mutable(strict=True)
class DangerZone(BaseConfigClass):
    svg_color_object: str = related.StringField(default="#ff0000")
    svg_color_person: str = related.StringField(default="#000080")
    svg_file: str = related.StringField(default="images/areas.svg")
    svg_scale_factor: float = related.IntegerField(default=10.0)

    @property
    def object_polygons(self) -> list[list[Point]]:
        return DangerZone.__load_svg(
            self.svg_file, self.svg_color_object, self.svg_scale_factor
        )

    @property
    def person_polygons(self) -> list[list[Point]]:
        return DangerZone.__load_svg(
            self.svg_file, self.svg_color_person, self.svg_scale_factor
        )

    @staticmethod
    @lru_cache
    def __load_svg(svg_path: str, color: str, scale: float) -> list[list[Point]]:
        doc = minidom.parse(svg_path)
        root = doc.getElementsByTagName("rect")
        polygons: list[list[Point]] = []
        for rect in root:
            rect_color = rect.getAttribute("style").split(";")[2].split(":")[1]
            if color == rect_color:
                width = int(float(rect.getAttribute("width")) * scale)
                height = int(float(rect.getAttribute("height")) * scale)
                x_pos = int(float(rect.getAttribute("x")) * scale)
                y_pos = int(float(rect.getAttribute("y")) * scale)
                poly: list[Point] = [
                    Point(x_pos, y_pos),
                    Point(x_pos + width, y_pos),
                    Point(x_pos + width, y_pos + height),
                    Point(x_pos, y_pos + height),
                ]
                polygons.append(poly)
        return polygons


@related.mutable(strict=True)
class MapBuilderConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    map_height: int = related.IntegerField(default=10000)
    map_width: int = related.IntegerField(default=8000)
    calc_per_seconds_map: int = related.IntegerField(default=10)
    calc_per_seconds_drawings: int = related.IntegerField(default=10)
    danger_zones: DangerZone = related.ChildField(cls=DangerZone, default=DangerZone())
    draw_calibration_points: bool = related.BooleanField(default=False)
    scale: float = related.FloatField(default=0.1)
    record: bool = related.BooleanField(default=False)


@related.mutable(strict=True)
class SensorFusionConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    map_height: int = related.IntegerField(default=10000)
    map_width: int = related.IntegerField(default=8000)
    calc_per_seconds: int = related.IntegerField(default=5)
    scale: float = related.FloatField(default=0.1)
    heat_map_cluster_size: int = related.IntegerField(default=10)
    heat_up_factor: int = related.IntegerField(default=1)
    cool_down_factor: int = related.IntegerField(default=2)
    danger_zones: DangerZone = related.ChildField(cls=DangerZone, default=DangerZone())


@related.mutable(strict=True)
class TransformerConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    map_height: int = related.IntegerField(default=10000)
    map_width: int = related.IntegerField(default=8000)
    add_calibration_points: bool = related.BooleanField(default=False)
    scale: float = related.FloatField(default=0.1)
    filter: str = related.StringField(default=".*")


@related.mutable(strict=True)
class MetricConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    batch_size: int = related.IntegerField(default=5)
    default_interval: int = related.IntegerField(default=5)
    influx_org: str = related.StringField(default="automodal")
    influx_token: str = related.StringField(default="supergeheimertoken")
    influx_url: str = related.StringField(default="localhost:8086")
    commit_in_db: bool = related.BooleanField(default=False)


@related.mutable(strict=True)
class LidarConfig(BaseConfigClass):
    writer_active: bool = related.BooleanField(default=False)
    name: str = related.StringField(default="lidar")
    compression: str = related.StringField(default="lz4")
    ip: str = related.StringField(default="127.0.0.1")
    data_port: int = related.IntegerField(default=2368)
    tele_port: int = related.IntegerField(default=8308)
    transformation_list: str = related.StringField(default="[0, 0, 0, 0]")
    rpm: int = related.IntegerField(default=600)
    active: bool = related.BooleanField(default=False)
    file_path: str = related.StringField(default="")

    @property
    def transformation(self) -> LidarTransformation:
        return LidarConfig.__get_transformation(self.transformation_list)

    @staticmethod
    @lru_cache
    def __get_transformation(transformation_list: str) -> LidarTransformation:
        data: list[float] = literal_eval(transformation_list)

        return LidarTransformation(*data)


@related.mutable(strict=True)
class LidarEnricherConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)


@related.mutable(strict=True)
class PublisherConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    image_scale: float = related.FloatField(default=-1.0)
    default_image_size_str: str = related.StringField(default="320x240")
    slowdown_factor: int = related.IntegerField(default=5)
    name: str = related.StringField(default="SAND")
    host: str = related.StringField(default="0.0.0.0")
    port: int = related.IntegerField(default=5000)

    communication: CommunicationConfig = related.ChildField(
        cls=CommunicationConfig,
        default=CommunicationConfig(),
        required=False,
    )

    @property
    def default_image_size(self) -> Dimensions:
        return PublisherConfig.__get_resolution(self.default_image_size_str)

    @staticmethod
    def __get_resolution(resolution_str: str) -> Dimensions:
        splitted = resolution_str.split("x")
        return Dimensions(int(splitted[0]), int(splitted[1]))


@related.mutable(strict=True)
class DriveWatcherConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    memory_remaining_gb: int = related.IntegerField(default=20)
    segment_length_secs: int = related.IntegerField(default=3600)
    folders: list[str] = related.SequenceField(cls=str, default=["recordings"])


@related.mutable(strict=True)
class ConverterConfig(BaseConfigClass):
    active: bool = related.BooleanField(default=False)
    folders: list[str] = related.SequenceField(cls=str, default=["recordings"])
    scan_interval_sec: int = related.IntegerField(default=300)
    scan_start_offset_sec: int = related.IntegerField(default=600)
    gpu_index: int = related.IntegerField(default=0)
    process_poll_interval_sec: int = related.IntegerField(default=10)
    delete_after_conversion: bool = related.BooleanField(default=False)
    speedup_visual: int = related.IntegerField(default=5)
    speedup_thermal: int = related.IntegerField(default=12)
    segment_length_sec: int = related.IntegerField(default=3600)


@related.mutable(strict=False)
class StatsConfig(BaseConfigClass):
    frames: FrameStatsConfig = related.ChildField(
        cls=FrameStatsConfig, default=FrameStatsConfig()
    )
    map: CraneMapStatsConfig = related.ChildField(
        cls=CraneMapStatsConfig, default=CraneMapStatsConfig()
    )


@related.mutable(strict=False)
class SandConfig(BaseConfigClass):
    cameras: list[CameraConfig] = related.SequenceField(
        cls=CameraConfig,
        default=[],
        required=False,
    )
    lidars: list[LidarConfig] = related.SequenceField(
        cls=LidarConfig,
        default=[],
        required=False,
    )
    lidar_enricher: LidarEnricherConfig = related.ChildField(
        cls=LidarEnricherConfig,
        default=LidarEnricherConfig(),
        required=False,
    )
    publisher: PublisherConfig = related.ChildField(
        cls=PublisherConfig,
        default=PublisherConfig(),
        required=False,
    )
    watcher: DriveWatcherConfig = related.ChildField(
        cls=DriveWatcherConfig,
        default=DriveWatcherConfig(),
        required=False,
    )
    metric: MetricConfig = related.ChildField(
        cls=MetricConfig,
        default=MetricConfig(),
        required=False,
    )
    converter: ConverterConfig = related.ChildField(
        cls=ConverterConfig,
        default=ConverterConfig(),
        required=False,
    )
    neural: NeuralNetworkConfig = related.ChildField(
        cls=NeuralNetworkConfig,
        default=NeuralNetworkConfig(),
        required=False,
    )
    transformer: TransformerConfig = related.ChildField(
        cls=TransformerConfig,
        default=TransformerConfig(),
        required=False,
    )
    map_builder: MapBuilderConfig = related.ChildField(
        cls=MapBuilderConfig,
        default=MapBuilderConfig(),
        required=False,
    )
    sensor_fusion: SensorFusionConfig = related.ChildField(
        cls=SensorFusionConfig,
        default=SensorFusionConfig(),
        required=False,
    )
    stats: StatsConfig = related.ChildField(
        cls=StatsConfig,
        default=StatsConfig(),
        required=False,
    )
    communication: CommunicationConfig = related.ChildField(
        cls=CommunicationConfig,
        default=CommunicationConfig(),
        required=False,
    )


ClassificationName = str
ClassificationId = int
DemoBoundingBox = List[int]
DemoDifficult = bool
DemoOccluded = bool
DemoContent = str
DemoScore = float
DemoBox = Tuple[
    ClassificationName,
    ClassificationId,
    DemoBoundingBox,
    DemoDifficult,
    DemoOccluded,
    DemoContent,
    DemoScore,
]


class ConstantConfig(RegisterAble):
    demo_boxes: DefaultDict[CameraName, list[DemoBox]] = defaultdict(
        lambda *x, **xx: [
            ("Person", 1, [1431, 267, 1664, 453], False, False, "", 1.0),
            ("PKW", 2, [1309, 225, 1496, 278], False, False, "", 1.0),
            ("LKW", 3, [1500, 300, 1564, 458], False, False, "", 1.0),
        ]
    )


def get_lidar_name(lidar_file: Path) -> str:
    possible_lidar_name = search(r"(f[1-4]_l[1-3]_[l][ia])(.velo)", lidar_file.name)

    if possible_lidar_name is None:
        return "invalid"
    return possible_lidar_name.group(1)


def _get_camera_dictionary(
    camera_file_expression: str, playback_path: Path
) -> dict[CameraName, Path]:
    video_files = playback_path.glob(camera_file_expression)
    video_dictionary = dict(
        list(map(lambda x: (get_camera_name(x.name, "invalid"), x), video_files))
    )

    log.d(f"Loading video_dictionary: {video_dictionary}", "_get_video_dictionary")
    return video_dictionary


def _get_lidar_dictionary(
    lidar_file_expression: str, playback_path: Path
) -> dict[CameraName, Path]:
    lidar_files = playback_path.glob(lidar_file_expression)
    lidar_dictionary = dict(list(map(lambda x: (get_lidar_name(x), x), lidar_files)))

    log.d(f"Loading lidar_dictionary: {lidar_dictionary}", "_get_lidar_dictionary")
    return lidar_dictionary


def _demo_boxes() -> None:
    constant_config = get_singleton_node(ConstantConfig)

    constant_config.demo_boxes["f1_l1_v1"] = [
        ("PKW", 1, [1431, 267, 1664, 453], False, False, "", 1.0),
        ("PKW", 1, [1309, 225, 1496, 278], False, False, "", 1.0),
        ("Person", 0, [1500, 300, 1564, 458], False, False, "", 1.0),
    ]
    constant_config.demo_boxes["f1_l2_v1"] = [
        ("Person", 0, [1443, 40, 1693, 305], False, False, "", 1.0),
        ("PKW", 1, [2282, 1338, 2557, 1440], False, False, "", 1.0),
    ]
    constant_config.demo_boxes["f1_l3_v1"] = [
        ("PKW", 1, [1940, 948, 2131, 1053], False, False, "", 1.0),
        ("LKW", 2, [300, 432, 1000, 555], False, False, "", 1.0),
    ]
    constant_config.demo_boxes["f1_l2_t1"] = [
        ("PKW", 1, [985, 0, 2048, 576], False, False, "", 1.0),
    ]
    constant_config.demo_boxes["f1_l3_t1"] = [
        ("PKW", 1, [682, 170, 754, 309], False, False, "", 1.0),
    ]

    log.i(f"Loaded box data: {constant_config.demo_boxes}", "_demo_boxes")


def change_to_playback_config(
    sand_config: SandConfig, playback_path: Path
) -> SandConfig:
    log.d(f"playback_path: {playback_path}", "change_to_playback_config")

    video_dictionary = _get_camera_dictionary(
        r"f[1-4]_l[1-3]_[vt][12]/*f[1-4]_l[1-3]_[vt][12]*.mp4", playback_path
    )

    if len(video_dictionary) == 0:
        video_dictionary = _get_camera_dictionary(
            r"f[1-4]_l[1-3]_[vt][12].jpg", playback_path
        )

        log.d(
            f"Loading video_dictionary:  {str(video_dictionary)}",
            "change_to_playback_config",
        )

        # for now deaktivated
        # _demo_boxes()

    for camera_config in sand_config.cameras:
        if camera_config.name in video_dictionary:
            camera_config.stream = (
                video_dictionary[camera_config.name].absolute().as_posix()
            )

    lidar_dictionary = _get_lidar_dictionary(
        r"f[1-4]_l[1-3]_[l][ia]/*f[1-4]_l[1-3]_[l][ia]*.velo", playback_path
    )

    log.d(
        f"Loading lidar_dictionary: {lidar_dictionary}",
        "change_to_playback_config",
    )

    for lidar_config in sand_config.lidars:
        if lidar_config.name in lidar_dictionary:
            lidar_config.file_path = lidar_dictionary[lidar_config.name].as_posix()

    return sand_config
