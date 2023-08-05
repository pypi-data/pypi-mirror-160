from __future__ import annotations

from sand.config import CommunicationConfig
from sand.reader.video import CameraSystem  # allowed
from sand.recorder.video.pipeline.normalizer import VideoNormalizer

from .writer import VideoWriter


class CameraRecorder:
    def __init__(
        self,
        camera_system: CameraSystem,
        communication_config: CommunicationConfig,
        playback: bool,
    ):
        if camera_system.config.writer_active:
            self.writer = VideoWriter(
                camera_system.config,
                communication_config,
                playback,
            )
            self.normalizer = VideoNormalizer(
                communication_config,
                camera_system,
                self.writer,
            )
