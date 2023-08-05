from __future__ import annotations

from cv2 import (
    COLOR_BGR2GRAY,
    INTER_AREA,
    THRESH_BINARY,
    bitwise_not,
    bitwise_or,
    cvtColor,
    imread,
    resize,
    threshold,
)
from numpy import zeros

from sand.util.time import now

from .frame import EnrichedFrame
from .types import Dimensions, Image


class AerialMap:
    _base_map: Image = imread("images/calibration.jpg")

    def __init__(
        self,
        frames: dict[str, EnrichedFrame],
        dimensions: Dimensions,
        scale: float,
        map_id: int,
    ) -> None:
        self.timestamp = now()  # creation time
        # Dict of all Enriched Frames in this AerialMap representation
        self.frames = frames
        self.scale = scale
        self.dimensions = dimensions
        self.map_id = map_id
        self.map: Image = zeros(
            (int(dimensions.height * self.scale), int(dimensions.width * self.scale), 3)
        )

    def __str__(self) -> str:
        return f"AerialMap: {{ timestamp: {self.timestamp}, }}"

    def add_frame(self, frame: Image) -> None:
        _th, mask = threshold(cvtColor(frame, COLOR_BGR2GRAY), 3, 255, THRESH_BINARY)
        self.map = frame + bitwise_or(self.map, self.map, mask=bitwise_not(mask))

    def add_base_map(self) -> None:
        self.add_frame(
            bitwise_not(
                resize(
                    AerialMap._base_map,
                    self.dimensions,
                    interpolation=INTER_AREA,
                )
            )
        )
