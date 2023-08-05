from __future__ import annotations

import re
from collections import deque
from threading import Lock
from time import sleep
from typing import Deque

from overrides import overrides

from sand.config import SandConfig, TransformerCombinationConfig
from sand.datatypes import Dimensions, EnrichedFrame
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.config.configuration_management import find_config
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import (
    CollectAble,
    EnrichedSubscriber,
    ImageTransformerSubscriber,
)
from sand.reader.video import FrameDecoder  # allowed
from sand.transformer.transformation import Transformation
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper


class ImageTransformer(
    SandNode,
    EnrichedSubscriber,
    CollectAble[ImageTransformerSubscriber],
    ConfigurationManager[TransformerCombinationConfig],
):
    def __init__(
        self,
        frame_decoder: FrameDecoder,
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

        self.queue: Deque[EnrichedFrame] = deque(maxlen=1)
        self.queue_lock = Lock()
        self.playback = playback
        self.subscribers: list[ImageTransformerSubscriber] = []
        self.source = FrameDecoder.__name__
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device=self.config.camera.name,
            expected=self.config.camera.fps,
        )
        self.dropped = PerSecondHelper(
            communicator=self,
            name="dropped",
            device=self.config.camera.name,
            expected=self.config.camera.fps,
        )

        frame_decoder.subscribe(self)

        self.transformer_helper = Transformation(self.config)

        self.create_thread(
            target=self.work,
            args=(),
            name="image_transformer",
            start=True,
        )

    @overrides
    def select_config(self, global_config: SandConfig) -> TransformerCombinationConfig:
        camera_config = find_config(self.camera_name, global_config.cameras)

        assert camera_config is not None

        return TransformerCombinationConfig(camera_config, global_config.transformer)

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        with self.queue_lock:
            self.dropped.add(float(len(self.queue)))
            self.queue.append(frame)

    @overrides
    def subscribe(self, subscriber: ImageTransformerSubscriber) -> None:
        self.subscribers.append(subscriber)

    def work(self) -> None:
        """
        we only transform cameras that matches the filter.
        that way we save resources. for example the map builder only needs
        transformations of the level 3 cameras
        but the detections of all other cameras must be transformed in any case
        """
        self.set_thread_name(self.__class__.__name__)
        pattern = re.compile(self.config.transformer.filter)
        while not self.shutdown_event.is_set():
            try:
                with self.queue_lock:
                    enriched_frame = self.queue.popleft()
                delta = DeltaHelper(
                    communicator=self,
                    device_name=enriched_frame.camera_name,
                    data_id=enriched_frame.id,
                    source=[self.source],
                )

                for subscriber in self.subscribers:
                    if pattern.match(enriched_frame.camera_name):
                        self.transformer_helper.transform_enriched_frame(enriched_frame)
                    subscriber.push_transformed_frame(enriched_frame)
                self.fps.inc_and_publish()
                self.dropped.publish()
                delta.set_end_and_publish()
            except IndexError:
                # this is somewhat expected, as we have a configured slowdown
                sleep(1 / self.config.camera.fps)
