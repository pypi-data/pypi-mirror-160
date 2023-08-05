from __future__ import annotations

from overrides import overrides

from sand.config import MapBuilderConfig, SandConfig
from sand.datatypes import EnrichedFrame, EnrichedLidarPacket
from sand.datatypes.aerialmap import AerialMap
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import (
    CollectAble,
    EnrichedSubscriber,
    ImageTransformerSubscriber,
)
from sand.map.build import build_map
from sand.registry import get_nodes
from sand.transformer.pipeline.image import ImageTransformer  # allowed
from sand.util.delta import DeltaHelper
from sand.util.per_second import PerSecondHelper
from sand.util.time import now
from sand.util.time_management import TimeManagement


class MapBuilder(
    SandNode,
    CollectAble[EnrichedSubscriber],
    ImageTransformerSubscriber,
    ConfigurationManager[MapBuilderConfig],
):
    images: dict[str, EnrichedFrame] = {}
    fusion_status: bool = False
    packet: EnrichedLidarPacket | None = None
    map: AerialMap | None = None

    def __init__(
        self,
        global_config: SandConfig,
        playback: bool,
    ):
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)
        self.subscribers: list[EnrichedSubscriber] = []

        self.playback = playback
        image_transformer = get_nodes(ImageTransformer)
        self.source = "ImageTransformer"
        for transformer in image_transformer:
            transformer.subscribe(self)

        self.time_management_map = TimeManagement(
            fps=self.config.calc_per_seconds_map,
            slowdown_factor=1,
            shutdown_event=self.shutdown_event,
        )
        # correctly it's calculations per second, but with fps the influx querys are way easier
        self.fps = PerSecondHelper(
            communicator=self,
            name="fps",
            device="all",
            expected=self.config.calc_per_seconds_map,
        )

        self.create_thread(
            target=self.work_map,
            args=(),
            name=f"wk_{self.__class__.__name__}",
            start=True,
        )

    @overrides
    def subscribe(self, subscriber: EnrichedSubscriber) -> None:
        self.subscribers.append(subscriber)

    @overrides
    def select_config(self, global_config: SandConfig) -> MapBuilderConfig:
        return global_config.map_builder

    @overrides
    def push_transformed_frame(self, frame: EnrichedFrame) -> None:
        self.images[frame.camera_name] = frame

    def work_map(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")
        map_id = 0
        self.log.d("map_builder worker thread started", "work_map")
        while not self.shutdown_event.is_set():
            if not self.time_management_map.wait_for_next_frame():
                self.log.d("shutdown occurred", "work_map")
                break

            map_id += 1
            delta = DeltaHelper(
                communicator=self,
                device_name="all",
                data_id=map_id,
                source=[self.source],
            )
            self.map = build_map(
                self.images,
                map_id,
                self.config.map_width,
                self.config.map_height,
                self.config.scale,
            )
            frame = EnrichedFrame("map_builder", now(), self.map.map)
            for sub in self.subscribers:
                sub.push_frame(frame)

            self.fps.inc_and_publish()
            delta.set_end_and_publish()
