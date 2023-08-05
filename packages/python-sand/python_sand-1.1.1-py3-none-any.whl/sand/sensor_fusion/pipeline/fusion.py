from __future__ import annotations

from copy import copy

from overrides import overrides

from sand.config import SandConfig, SensorFusionConfig
from sand.datatypes import Box, LidarPoints, Point, Topic, TransformedBoxes
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.neural.third_party.mlcvzoo.bounding_box import BoundingBox  # allowed
from sand.sensor_fusion.checker import Checker
from sand.util.boxes import approximation
from sand.util.camera import get_level
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper
from sand.util.time_management import TimeManagement


class SensorFusion(SandNode, ConfigurationManager[SensorFusionConfig]):
    boxes: dict[Topic, TransformedBoxes] = {}
    pointcloud2d: dict[str, LidarPoints] = {}

    def __init__(self, global_config: SandConfig):
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(
            self,
            self,
            global_config,
            update_pattern=f"{ConfigurationManager.__name__}/.*/data/sensor_fusion/.*",
        )

        self.time_management = TimeManagement(
            fps=self.config.calc_per_seconds,
            slowdown_factor=1,
            shutdown_event=self.shutdown_event,
        )

        self.checker = Checker(self.config)

        self.source = ["BoxTransformer", "LidarPacketEnricher"]
        self.subscribe_topic(
            "BoxTransformer/+/data/transformed_boxes", self.push_box_frame
        )
        self.subscribe_topic(
            "LidarPacketEnricher/+/data/pointcloud2d",
            self.push_pointcloud2d,
        )

        self.calc_per_seconds = PerSecondHelper(
            communicator=self,
            name="cals_per_seconds",
            device="all",
            expected=self.config.calc_per_seconds,
        )
        self.collisions_per_second = PerSecondHelper(
            communicator=self, name="collisions_per_second", device="all"
        )

        self.create_thread(
            target=self.work,
            name=self.__class__.__name__,
            start=True,
        )

    @overrides
    def select_config(self, global_config: SandConfig) -> SensorFusionConfig:
        return global_config.sensor_fusion

    @overrides
    def config_has_updated(self) -> None:
        self.checker.reinit_data(self.config)

    def push_box_frame(self, topic: Topic, payload: TransformedBoxes) -> None:
        self.boxes[topic] = payload

    def push_pointcloud2d(self, topic: Topic, payload: LidarPoints) -> None:
        camera = topic.split("/")[1]
        self.pointcloud2d[camera] = payload

    def check_collision(self, box: Box, class_name: str) -> bool:
        try:
            if class_name == "person":
                return self.checker.test_person(box)
            return self.checker.test_box(box)
        except IndexError:
            self.log.exception("uncatched indexError", "check_collision")
            return False

    def test_box_list(
        self,
        box_list: list[Box],
        bounding_boxes: list[BoundingBox],
        camera_name: str,
    ) -> bool:
        collision = False
        box_list_corrected = []
        for index, value in enumerate(box_list):
            # if index not in detections, than theres additional boxes, but not from the neural net. so we ignore them
            corrected = approximation(value) if get_level(camera_name) == 1 else value
            box_list_corrected.append(corrected)
            if index < len(bounding_boxes) and self.check_collision(
                corrected, bounding_boxes[index].class_name.lower()
            ):
                collision = True
        return collision

    def work(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")
        fusion_id = 0
        while not self.shutdown_event.is_set():
            # work only every 1/x seconds
            if not self.time_management.wait_for_next_frame():
                self.log.d("shutdown occurred", "work")
                break

            fusion_id += 1
            delta = DeltaHelper(
                communicator=self,
                device_name="all",
                data_id=fusion_id,
                source=self.source,
            )
            collisions = 0
            self.checker.reset_collision()

            for _, transformed_boxes in list(self.boxes.items()):
                collisions += int(
                    self.test_box_list(
                        transformed_boxes.transformed_boxes,
                        transformed_boxes.boxes,
                        transformed_boxes.camera_name,
                    )
                )

            for _, pointcloud in copy(self.pointcloud2d).items():
                for point in pointcloud:
                    point_x = int((point[0] * 100 + 4050) * self.config.scale)
                    point_y = int((point[1] * 100 + 2710) * self.config.scale)
                    self.checker.test_point(Point(point_x, point_y))

            self.publish(
                payload=self.checker.get_collision_map(),
                topic=f"{SensorFusion.__name__}/all/data/collision_map",
            )
            self.publish(
                payload=collisions > 0,
                topic=f"{SensorFusion.__name__}/all/data/collision",
                retain=True,
            )
            self.publish(
                payload=collisions,
                topic=f"{SensorFusion.__name__}/all/data/collision_count",
            )
            for key, heat_map in self.checker.get_heat_maps().items():
                heat_map.calc()
                self.publish(
                    payload=heat_map.current_state,
                    topic=f"{SensorFusion.__name__}/all/data/heat_map_{key}",
                )
            delta.set_end_and_publish()
            self.calc_per_seconds.inc_and_publish()
            self.collisions_per_second.add_and_publish(collisions)
