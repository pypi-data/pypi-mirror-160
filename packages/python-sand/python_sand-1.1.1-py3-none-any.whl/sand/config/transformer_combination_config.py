from __future__ import annotations

from typing import NamedTuple

from .config import CameraConfig, TransformerConfig


class TransformerCombinationConfig(NamedTuple):
    camera: CameraConfig
    transformer: TransformerConfig
