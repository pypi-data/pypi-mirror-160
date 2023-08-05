from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Delta:
    id: int
    device_name: str
    type: str
    source: str
    start: float
    end: float
