from __future__ import annotations

from collections import deque
from threading import Lock
from time import sleep
from typing import Deque

from cv2 import perspectiveTransform
from nptyping import Float, NDArray, Shape
from numpy import array
from overrides import overrides

from sand.config import SandConfig, TransformerCombinationConfig
from sand.datatypes import (
    Box,
    Dimensions,
    EnrichedFrame,
    Point,
    SandBoxes,
    Topic,
    TransformedBoxes,
)
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.config.configuration_management import find_config
from sand.interfaces.synchronization import SandNode
from sand.neural.third_party.mlcvzoo.bounding_box import BoundingBox  # allowed
from sand.transformer.focal import FocalNormalizer
from sand.transformer.transformation import Transformation
from sand.util.boxes import bounding_box_to_point_list
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper


class BoxTransformer(SandNode, ConfigurationManager[TransformerCombinationConfig]):
    def __init__(
        self,
        camera_name: str,
        global_config: SandConfig,
        playback: bool,
    ) -> None:
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        self.camera_name = camera_name
        EnrichedFrame.map_size = Dimensions(
            self.config.transformer.map_width, self.config.transformer.map_height
        )

        self.queue: Deque[SandBoxes] = deque(maxlen=1)
        self.queue_lock = Lock()
        self.playback = playback
        self.source = "NeuralNetwork"
        self.box_per_second = PerSecondHelper(
            communicator=self,
            name="box_per_second",
            device=self.config.camera.name,
            expected=self.config.camera.fps,
        )
        self.dropped = PerSecondHelper(
            communicator=self,
            name="dropped",
            device=self.config.camera.name,
            expected=self.config.camera.fps,
        )

        self.subscribe_topic(
            f"{self.source}/{self.config.camera.name}/data/boxes",
            self.push_neural_frame,
        )

        self.transformation = Transformation(self.config)
        self.focal = FocalNormalizer(self.config.camera.focal)

        if self.config.transformer.active:
            self.create_thread(
                target=self.work,
                args=(),
                name=self.get_name(),
                start=True,
            )

    @overrides
    def select_config(self, global_config: SandConfig) -> TransformerCombinationConfig:
        camera_config = find_config(
            device_name=self.camera_name, config_list=global_config.cameras
        )

        assert camera_config is not None

        return TransformerCombinationConfig(
            camera=camera_config,
            transformer=global_config.transformer,
        )

    def push_neural_frame(self, _: Topic, boxes: SandBoxes) -> None:
        if len(boxes.boxes) > 0:
            with self.queue_lock:
                self.dropped.add(float(len(self.queue)))
                self.queue.append(boxes)

    def get_name(self) -> str:
        return f"bt_{self.config.camera.name}"

    def _transform_bounding_box(self, bounding_box: BoundingBox) -> Box | None:

        # use the focal distortion map to undistort the points
        focal_points: list[Point] = []
        box_points = bounding_box_to_point_list(bounding_box, (2560, 1440))
        for point in box_points:
            if int(point.y) < len(self.focal.map_x) and int(point.x) < len(
                self.focal.map_x[point.y]
            ):
                focal_point = self.focal.map_x[int(point.y)][int(point.x)]
                focal_points.append(Point(focal_point[0], focal_point[1]))
            else:
                self.log.d(
                    f"{int(point.x)=} < {len(self.focal.map_y)=} and {int(point.y)=} < {len(self.focal.map_x)=}",
                    "_transform_bounding_box",
                )
        # the transformation
        # we need the right array format for transformation
        np_points = array([focal_points], dtype="float32")
        if np_points.shape[1] != 4:
            self.log.d(
                f"points are not len 4 - {np_points=}, {focal_points=}, {box_points=}, {bounding_box=}",
                "_transform_bounding_box",
            )
            return None

        transformed_points: NDArray[
            Shape["4 points, [x, y]"], Float
        ] = perspectiveTransform(np_points, self.transformation.get_matrix())
        # scaling is not necessary, the transformation matrix is generated with the right scale
        int_points = transformed_points.astype(int)[0]
        output_points = list(map(lambda pt: Point(pt[0], pt[1]), int_points))
        if len(output_points) != 4:
            self.log.d(
                f"transformed points are not len 4 - len(output_points): {len(output_points)}",
                "_transform_bounding_box",
            )
            return None
        return Box(*output_points)

    def _transform_cal_points(self, point_list: list[Point]) -> list[Point] | None:
        if len(point_list) == 0:
            return None
        # the transformation
        # we need the right array format for transformation
        transformed_points: NDArray[
            Shape["4 points, [x, y]"], Float
        ] = perspectiveTransform(
            array([point_list], dtype="float32"), self.transformation.get_matrix()
        )
        # scaling is not necessary, the transformation matrix is generated with the right scale
        int_points = transformed_points.astype(int)[0]
        return list(map(lambda pt: Point(pt[0], pt[1]), int_points))

    def _get_calibration_points(self) -> list[Point] | None:
        cal_points = self._transform_cal_points(
            self.config.camera.transformation.source_points
        )
        return cal_points

    def _transform_boxes(self, boxes: list[BoundingBox]) -> list[Box]:
        output = []
        for box in boxes:
            transformed_box = self._transform_bounding_box(box)
            if transformed_box is not None:
                output.append(transformed_box)
        return output

    def work(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")

        self.log.i("Starting to work", "work")

        while not self.shutdown_event.is_set():
            try:
                with self.queue_lock:
                    box = self.queue.popleft()
                delta = DeltaHelper(
                    communicator=self,
                    device_name=box.camera_name,
                    data_id=box.frame_id,
                    source=[self.source],
                )
                self.focal.check_init(box.width, box.height)

                transformed_boxes = self._transform_boxes(box.boxes)
                result = TransformedBoxes(
                    box.frame_id,
                    box.timestamp,
                    box.camera_name,
                    box.boxes,
                    transformed_boxes,
                )
                self.publish(
                    payload=result,
                    topic=f"{BoxTransformer.__name__}/{self.config.camera.name}/data/transformed_boxes",
                )

                if self.config.transformer.add_calibration_points:
                    cal_points = self._get_calibration_points()
                    if cal_points is not None:
                        self.publish(
                            payload=cal_points,
                            topic=f"{BoxTransformer.__name__}/{self.config.camera.name}/data/transformed_calibration_points",
                        )

                self.box_per_second.inc_and_publish()
                delta.set_end_and_publish()

            except IndexError as exception:
                if "pop from an empty deque" not in exception.args:
                    # exception gives stacktrace
                    self.log.exception(str(exception.args), "work")
                sleep(1 / self.config.camera.fps)
