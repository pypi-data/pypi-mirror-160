from __future__ import annotations

from overrides import overrides

from sand.config import CameraConfig, SandConfig
from sand.datatypes import EnrichedFrame
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import EnrichedSubscriber
from sand.map import MapEnricher  # allowed
from sand.recorder.video.pipeline import VideoNormalizer, VideoWriter


class MapRecorder(EnrichedSubscriber, SandNode):
    def __init__(self, sand_config: SandConfig, map_enricher: MapEnricher):
        SandNode.__init__(self, sand_config.communication)

        # pylint: disable=unexpected-keyword-arg
        self.config = CameraConfig(  # type: ignore[call-arg]
            writer_active=True,
            fps=5,
            name="map",
            stream="invalid",
            interesting_mode="off",
        )

        self.writer = VideoWriter(
            self.config, sand_config.communication, playback=False
        )
        self.normalizer = VideoNormalizer(
            camera_system=None,
            writer=self.writer,
            communication_config=sand_config.communication,
        )

        self.log.i("Starting recording", "__init__")
        map_enricher.subscribe(self)

        # activate map combining system
        self.publish(
            payload=True,
            topic=f"{MapRecorder.__name__}/all/data/active",
            retain=True,
        )

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        frame = EnrichedFrame(
            camera_name="map",
            timestamp=frame.timestamp,
            frame=frame.frame,
        )

        self.normalizer.push_frame(frame)
