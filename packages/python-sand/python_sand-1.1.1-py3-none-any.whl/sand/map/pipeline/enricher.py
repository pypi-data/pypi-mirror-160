from __future__ import annotations

from copy import copy, deepcopy

from overrides import overrides

from sand.config import MapBuilderConfig, SandConfig
from sand.datatypes import (
    Box,
    CollisionMap,
    Color,
    EnrichedFrame,
    LidarPoints,
    Point,
    Topic,
    TransformedBoxes,
)
from sand.datatypes.aerialmap import AerialMap
from sand.datatypes.types import HeatMapArray
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import CollectAble, EnrichedSubscriber
from sand.util.boxes import (
    approximation,
    get_box_center,
    scale_point_list,
    scale_transformed_boxes,
)
from sand.util.camera import get_level
from sand.util.color import camera_colors_by_level, get_color, get_lidar_color
from sand.util.delta import DeltaHelper
from sand.util.image import (
    add_text_to_image,
    draw_circle,
    draw_detection_box,
    draw_heat_map,
    draw_polygon,
    draw_x,
)
from sand.util.per_second import PerSecondHelper
from sand.util.time import now
from sand.util.time_management import TimeManagement

from .builder import MapBuilder


class MapEnricher(
    SandNode, CollectAble[EnrichedSubscriber], ConfigurationManager[MapBuilderConfig]
):
    collision: CollisionMap | None = None
    heat_maps: dict[str, HeatMapArray] = {}
    heat_map_colors = [Color(255, 0, 0), Color(0, 255, 0)]
    boxes: dict[str, TransformedBoxes] = {}
    cal_points: dict[str, list[Point]] = {}
    fusion_status: bool = False
    pointcloud2d: dict[str, LidarPoints] = {}

    def __init__(
        self, global_config: SandConfig, playback: bool, map_builder: MapBuilder
    ):
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        self.playback = playback
        self.map_builder = map_builder

        self.source = [
            "BoxTransformer",
            "SensorFusion",
            "LidarPacketEnricher",
        ]
        self.subscribe_topic(
            "BoxTransformer/+/data/transformed_boxes", self._push_boxes
        )
        self.subscribe_topic(
            "BoxTransformer/+/data/transformed_calibration_points",
            self._push_cal_points,
        )
        self.subscribe_topic(
            "SensorFusion/all/data/collision_map", self._push_collision
        )
        self.subscribe_topic(
            "SensorFusion/all/data/heat_map_pointcloud", self._push_heat_map
        )
        self.subscribe_topic(
            "SensorFusion/all/data/heat_map_detection", self._push_heat_map
        )
        self.subscribe_topic(
            "SensorFusion/all/data/collision", self._push_fusion_status
        )
        self.subscribe_topic(
            "LidarPacketEnricher/+/data/pointcloud2d",
            self._push_pointcloud2d,
        )

        self.subscribers: list[EnrichedSubscriber] = []

        self.time_management_draw = TimeManagement(
            fps=self.config.calc_per_seconds_drawings,
            slowdown_factor=1,
            shutdown_event=self.shutdown_event,
        )

        # correctly it's calculations per second, but with fps the influx queries are way easier
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device="all",
            expected=self.config.calc_per_seconds_drawings,
        )

        self.create_thread(
            target=self.work_draw,
            args=(),
            name=self.__class__.__name__,
            start=True,
        )

    @overrides
    def select_config(self, global_config: SandConfig) -> MapBuilderConfig:
        return global_config.map_builder

    def _push_fusion_status(self, _: Topic, payload: bool) -> None:
        self.fusion_status = payload

    def _push_heat_map(self, topic: Topic, payload: HeatMapArray) -> None:
        name = topic.split("/")[3].split("_")[2]
        self.heat_maps[name] = payload

    def _push_pointcloud2d(self, topic: Topic, payload: LidarPoints) -> None:
        camera = topic.split("/")[1]
        self.pointcloud2d[camera] = payload

    def _push_boxes(self, topic: Topic, payload: TransformedBoxes) -> None:
        camera = topic.split("/")[1]
        self.boxes[camera] = payload

    def _push_cal_points(self, topic: Topic, payload: list[Point]) -> None:
        camera = topic.split("/")[1]
        self.cal_points[camera] = payload

    def _push_collision(self, _: Topic, payload: CollisionMap) -> None:
        self.collision = payload

    @overrides
    def subscribe(self, subscriber: EnrichedSubscriber) -> None:
        self.subscribers.append(subscriber)

    def draw_detections(self, terminal_map: AerialMap, camera: str) -> None:
        if camera not in self.boxes:
            self.log.w(f"{camera} is not in self.boxes", "draw_detections")
            return

        # save current state, so it doesn't change while working on it
        current_detections = self.boxes[camera]

        boxes = scale_transformed_boxes(
            current_detections.transformed_boxes, self.config.scale
        )
        detection = current_detections.boxes
        for box_index, box in enumerate(boxes):
            if len(box) != 4:
                self.log.w(
                    f"{camera} boxes don't have 4 points, length: {len(boxes)} | boxes: {box}",
                    "draw_boxes_and_points",
                )
                continue

            # correct the camera on l1
            corrected_box = approximation(box) if get_level(camera) == 1 else box
            is_person = detection[box_index].class_name.lower() == "person"
            if is_person:
                self.draw_person_detection(
                    terminal_map, corrected_box, get_color(camera)
                )
                terminal_map.map = draw_detection_box(
                    terminal_map.map, corrected_box, Color(200, 200, 200), 1
                )
            else:
                terminal_map.map = draw_detection_box(
                    terminal_map.map, corrected_box, get_color(camera), 2
                )

    def draw_cal_points(self, terminal_map: AerialMap, camera: str) -> None:
        if camera not in self.cal_points:
            self.log.w(f"{camera} is not in self.cal_points", "draw_cal_points")
            return
        for point in scale_point_list(self.cal_points[camera], self.config.scale):
            terminal_map.map = draw_x(
                terminal_map.map, int(point.x), int(point.y), get_color(camera)
            )

    def draw_danger_zones(
        self, terminal_map: AerialMap, polygons: list[list[Point]], color: Color
    ) -> None:
        for polygon in polygons:
            scaled_polygon = list(
                map(
                    lambda p: Point(
                        int(p.x * self.config.scale), int(p.y * self.config.scale)
                    ),
                    polygon,
                )
            )
            terminal_map.map = draw_polygon(
                terminal_map.map, scaled_polygon, color, fill=True
            )

    def draw_person_detection(
        self, terminal_map: AerialMap, box: Box, color: Color
    ) -> None:
        person_radius = int(self.config.scale * 75)
        terminal_map.map = draw_circle(
            terminal_map.map,
            get_box_center(box),
            person_radius,
            color,
        )

    @staticmethod
    def draw_collisions(terminal_map: AerialMap, collisions_map: CollisionMap) -> None:
        # pylint: disable=consider-using-enumerate
        for y_id in range(0, len(collisions_map)):
            for x_id in range(0, len(collisions_map[y_id])):
                if collisions_map[y_id][x_id]:
                    draw_circle(
                        terminal_map.map,
                        Point(x_id, y_id),
                        radius=2,
                        color=Color(0, 0, 255),
                        line_width=1,
                    )

    def draw_pointcloud2d(self, terminal_map: AerialMap, lidar_name: str) -> None:
        color = get_lidar_color(lidar_name)
        for point in self.pointcloud2d[lidar_name]:
            point_x = int((point[0] * 100) * self.config.scale)
            point_y = int((point[1] * 100) * self.config.scale)
            if point_y < len(terminal_map.map) and point_x < len(
                terminal_map.map[point_y]
            ):
                terminal_map.map[point_y][point_x] = color

    def draw_meta(self, terminal_map: AerialMap) -> None:
        # sensor fusion
        status = "OK"
        if self.fusion_status:
            status = "collision!!!"
        add_text_to_image(
            terminal_map.map,
            f"Fusion Status: {status}",
            Point(int(100 * self.config.scale), int(50)),
            font_scale=10 * self.config.scale,
            color=Color(0, 0, 255),
            thickness=2,
            copy=False,
        )
        # layer colors
        for level in range(1, 4):
            add_text_to_image(
                terminal_map.map,
                f"Level{level}",
                Point(int(100 * self.config.scale), int(50 + (50 * level))),
                font_scale=10 * self.config.scale,
                color=camera_colors_by_level[level],
                thickness=2,
                copy=False,
            )

    def print_map_info(
        self,
        terminal_map: AerialMap,
    ) -> None:
        self.log.d(
            f"size: {len(terminal_map.map)} {len(terminal_map.map[0])}", "map_info"
        )
        self.log.d(f"type: {type(terminal_map.map[0][0][0])}", "map_info")

    def draw_on_map(self, terminal_map: AerialMap) -> AerialMap:

        # add the danger zones
        self.draw_danger_zones(
            terminal_map, self.config.danger_zones.object_polygons, Color(0, 127, 127)
        )
        self.draw_danger_zones(
            terminal_map, self.config.danger_zones.person_polygons, Color(0, 0, 255)
        )
        for heat_map_id, (_name, heat_map) in enumerate(self.heat_maps.items()):
            terminal_map.map = draw_heat_map(
                terminal_map.map, heat_map, self.heat_map_colors[heat_map_id]
            )
        # add lidar points
        # 0,0 is at x = 5000,y = 2700
        for lidar_name in copy(self.pointcloud2d):
            self.draw_pointcloud2d(terminal_map, lidar_name)

        # add detections (boxes or circles)
        for camera in copy(self.boxes):
            self.draw_detections(terminal_map, camera)

        # add calibration points
        if self.config.draw_calibration_points:
            for cal_point in copy(self.cal_points):
                self.draw_cal_points(terminal_map, cal_point)

        # add the calibration image on top
        # terminal_map.add_base_map()
        if self.collision is not None:
            MapEnricher.draw_collisions(terminal_map, self.collision)
        self.draw_meta(terminal_map)

        return terminal_map

    def work_draw(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")
        self.log.d("map_enricher worker thread started", "work_draw")
        while not self.shutdown_event.is_set():
            if not self.time_management_draw.wait_for_next_frame():
                self.log.d("shutdown occurred", "work_draw")
                break

            if self.map_builder.map is not None:
                delta = DeltaHelper(
                    communicator=self,
                    device_name="all",
                    data_id=self.map_builder.map.map_id,
                    source=self.source,
                )
                drawn_map = self.draw_on_map(deepcopy(self.map_builder.map))
                frame = EnrichedFrame("map_enricher", now(), drawn_map.map)
                for sub in self.subscribers:
                    sub.push_frame(frame)
                self.fps.inc_and_publish()
                delta.set_end_and_publish()
