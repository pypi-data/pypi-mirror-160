from __future__ import annotations

import numpy
from cv2 import INTER_NEAREST, getPerspectiveTransform, warpPerspective
from numpy import array

from sand.config import TransformerCombinationConfig
from sand.datatypes import CalPoints, EnrichedFrame, Image, Matrix
from sand.transformer.focal import FocalNormalizer


# Works with the EnrichedFrame Pointer
class Transformation:
    def __init__(self, config: TransformerCombinationConfig) -> None:
        self.config = config
        self.set_focal(self.config.camera.focal)
        self.set_cal_points(self.config.camera.transformation)
        self.scale = 1

    def _calc_matrix(self) -> Matrix:
        source_points, target_points = self.calpoints
        if len(target_points) == 4 and len(source_points) == 4:
            return getPerspectiveTransform(  # type: ignore[no-any-return]
                numpy.float32(source_points),  # type: ignore[arg-type]
                numpy.float32(target_points),  # type: ignore[arg-type]
            )
        return array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def get_matrix(self) -> Matrix:
        return self.matrix

    def set_cal_points(self, calpoints: CalPoints) -> None:
        self.calpoints = calpoints
        self.matrix: Matrix = self._calc_matrix()

    def set_focal(self, focal: int) -> None:
        self.focal = FocalNormalizer(focal)

    def transform_enriched_frame(self, frame: EnrichedFrame) -> None:
        output = self.focal.normalize_enriched_frame(frame)  # cached
        matrix = self.get_matrix()  # cached
        frame.mapped_frame = warpPerspective(
            output,
            matrix,
            (self.config.transformer.map_width, self.config.transformer.map_height),
            flags=INTER_NEAREST,
        )

    def transform_image(self, image: Image) -> Image:
        output = self.focal.normalize_image(image)  # cached
        matrix = self.get_matrix()  # cached
        return warpPerspective(  # type: ignore[no-any-return]
            output,
            matrix,
            (self.config.transformer.map_width, self.config.transformer.map_height),
            flags=INTER_NEAREST,
        )
