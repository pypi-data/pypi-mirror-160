from __future__ import annotations

import time
from collections import defaultdict
from pathlib import Path
from threading import Lock
from time import sleep
from typing import DefaultDict, Dict, cast

import yaml
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.model import Model, ObjectDetectionModel
from mlcvzoo_base.models.model_registry import ModelRegistry
from overrides import overrides

from sand.config import ConstantConfig, NeuralNetworkConfig, SandConfig
from sand.datatypes import EnrichedFrame, SandBoxes
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import EnrichedSubscriber
from sand.reader.video import CameraSystem  # allowed
from sand.registry import get_singleton_node
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper


class CameraList:
    def __init__(self, cameras: list[str]) -> None:
        # TODO: think about prioritization between cameras, i.e. sea-side is not important -> 1/2 fps?
        self.all_cameras = cameras
        self.__current_index = 0

    def next(self) -> str:
        result = self.all_cameras[self.__current_index]
        # round-robin
        self.__current_index = (self.__current_index + 1) % len(self.all_cameras)
        return result


class NeuralNetwork(
    EnrichedSubscriber, SandNode, ConfigurationManager[NeuralNetworkConfig]
):
    def __init__(
        self,
        camera_systems: list[CameraSystem],
        global_config: SandConfig,
    ):
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        self.camera_list = CameraList(
            list(map(lambda cs: cs.config.name, camera_systems))
        )
        self.images: DefaultDict[str, EnrichedFrame | None] = defaultdict(lambda: None)
        self.constant_config = get_singleton_node(ConstantConfig)
        self.image_lock = Lock()
        self.started = False

        # correctly it's detections per second, but with fps the influx queries are way easier
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=NeuralNetwork.__name__,
            expected=0,
        )
        self.dropped = PerSecondHelper(
            communicator=self,
            name="dropped",
            device=NeuralNetwork.__name__,
            expected=0,
        )

        self.create_thread(
            target=self.work,
            args=(),
            name=NeuralNetwork.__name__,
            start=False,
        )

        if (
            not self.config.demo
            and self.config.active
            and self.config.model_config is not None
        ):
            replacement_map = self.get_mlcvzoo_replacement_map(
                replacement_config_path=Path(self.config.replacement_config_path)
                if self.config.replacement_config_path is not None
                else None
            )

            model_registry = ModelRegistry()

            model: Model = model_registry.init_model(  # type: ignore[type-arg]
                model_config=self.config.model_config,
                string_replacement_map=replacement_map,
            )

            if not isinstance(model, ObjectDetectionModel):
                raise ValueError(
                    "Currently only models that inherit from "
                    "'mlcvzoo_base.api.model.ObjectDetectionModel' "
                    "are allowed in the neural.model_config"
                )

            self.model: ObjectDetectionModel = model  # type: ignore[type-arg]

            # TODO: fix call of num_classes when mlcvzoo has solved the bug
            self.publish(
                payload=self.model.num_classes
                if isinstance(self.model.num_classes, int)
                else self.model.num_classes(),  # type: ignore[operator]
                topic=f"{NeuralNetwork.__name__}/all/data/num_classes",
                retain=True,
            )

        self.sources = list(
            map(
                lambda camera_name: f"CameraReader_{camera_name}",
                self.camera_list.all_cameras,
            )
        )

        for camera_system in camera_systems:
            camera_system.reader.subscribe(self)

    @staticmethod
    def get_mlcvzoo_replacement_map(
        replacement_config_path: Path | None,
    ) -> dict[str, str]:

        if replacement_config_path is None:
            return {}

        with replacement_config_path.open() as replacement_config:
            return cast(
                Dict[str, str], yaml.load(replacement_config, Loader=yaml.FullLoader)
            )

    @overrides
    def select_config(self, global_config: SandConfig) -> NeuralNetworkConfig:
        return global_config.neural

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        if not self.config.active:
            return

        if not self.started:
            self.started = True
            self.start_all_threads()

        with self.image_lock:
            # overrides, meaning not all will be checked
            was_dropped = self.images[frame.camera_name] is not None
            self.images[frame.camera_name] = frame

        # do outside the locked environment
        if was_dropped:
            self.dropped.add(1)

    def work(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")
        skip_counter = 0
        while not self.shutdown_event.is_set():
            current_camera = self.camera_list.next()
            with self.image_lock:
                enriched_frame = self.images[current_camera]
                self.images[current_camera] = None

            if enriched_frame is None:
                if skip_counter > len(self.camera_list.all_cameras):
                    self.log.i(
                        "Skipped all cameras once in a row, sleeping shortly...", "work"
                    )
                    # pause if we skipped all the current frames
                    # otherwise jump straight to the next one
                    skip_counter = 0
                    sleep(self.config.wait_time_no_image_available)
                skip_counter += 1
                continue

            skip_counter = 0

            delta = DeltaHelper(
                communicator=self,
                source=self.sources,
                device_name=current_camera,
                data_id=enriched_frame.id,
            )
            boxes: list[BoundingBox]

            if self.config.demo:
                data = self.constant_config.demo_boxes[current_camera]

                boxes = list(
                    map(
                        lambda box: BoundingBox(
                            class_identifier=ClassIdentifier(
                                class_name=box[0],
                                class_id=box[1],
                            ),
                            box=Box(
                                xmin=box[2][0],
                                ymin=box[2][1],
                                xmax=box[2][2],
                                ymax=box[2][3],
                            ),
                            difficult=box[3],
                            occluded=box[4],
                            content=box[5],
                            score=box[6],
                        ),
                        data,
                    )
                )
                time.sleep(0.5)
            else:
                assert isinstance(self.model, ObjectDetectionModel)
                _, bounding_boxes = self.model.predict(data_item=enriched_frame.frame)
                boxes = bounding_boxes

            box_msg = SandBoxes(
                enriched_frame.id,
                current_camera,
                enriched_frame.timestamp,
                boxes,  # type: ignore[arg-type]
                enriched_frame.width,
                enriched_frame.height,
            )

            self.publish(
                payload=box_msg,
                topic=f"{NeuralNetwork.__name__}/{current_camera}/data/boxes",
            )
            self.fps.inc_and_publish()
            self.dropped.publish()

            if self.config.log_detections:
                self.log.i(
                    message=f"Detections for n_{current_camera}: {boxes}",
                    tag="work",
                )

            if any(map(lambda box: box.class_name.lower() == "person", boxes)):
                self.publish(
                    payload=enriched_frame.timestamp,
                    topic=f"{NeuralNetwork.__name__}/{current_camera}/data/interesting",
                    retain=True,
                )
            delta.set_end_and_publish()
