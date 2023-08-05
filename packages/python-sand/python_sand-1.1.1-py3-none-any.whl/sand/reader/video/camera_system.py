from __future__ import annotations

import prctl

from sand.config import CameraConfig, SandConfig
from sand.view.stream.pipeline.stream_server import StreamServer  # allowed

from .encoder import FrameEncoder
from .reader import CameraReader


class CameraSystem:
    def __init__(
        self,
        reader_config: CameraConfig,
        sand_config: SandConfig,
        playback: bool,
    ):
        self.config = reader_config
        self.reader = CameraReader(reader_config, sand_config.communication, playback)
        self.encoder = FrameEncoder(
            reader_config,
            sand_config.communication,
            self.reader,
        )
        if self.config.serve_stream:
            self.server = StreamServer(
                reader_config.name,
                reader_config.serve_port,
                reader_config.stream_resolution,
                sand_config.communication,
                self.reader,
            )
        prctl.set_proctitle(f"SAND_Camera_System_{self.config.name}")
        prctl.set_name(f"SAND_Camera_System_{self.config.name}")

    def start(self) -> None:
        self.reader.start()
