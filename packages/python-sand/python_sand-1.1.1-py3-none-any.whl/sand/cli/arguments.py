from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from sand.logger.mqtt_logger import MQTTLoggerListener


class Arguments(NamedTuple):
    config: Path
    logger_listener: MQTTLoggerListener | None
    playback: Path | None
    check: bool
    gpus: int
    ignore_on_shutdown: bool
    custom_start_module: str
