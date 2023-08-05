from __future__ import annotations

import numpy
from cv2 import BORDER_CONSTANT, CV_16SC2, INTER_LINEAR, remap
from cv2.fisheye import initUndistortRectifyMap
from numpy import array, eye

from sand.datatypes import EnrichedFrame, Image, Matrix


class FocalNormalizer:
    def __init__(self, focal: int) -> None:
        self.focal = focal
        self.distortion_coefficients = array([[0], [0], [0], [0]], dtype=numpy.float32)
        self.camera_intrinsic_matrix: Matrix | None = None
        self.map_x = FocalNormalizer._get_default_focal_map()
        self.map_y = FocalNormalizer._get_default_focal_map()
        self.map_init = False

    @staticmethod
    def _get_default_focal_map() -> list[list[list[int]]]:
        # könnte man zukünftig auch auf die größe der map initialisieren.
        # Aber unklar woher widht/height kommen könnte.
        focal_map = []
        for outer in range(0, 10):
            row = []
            for inner in range(0, 10):
                row.append([inner, outer])
            focal_map.append(row)
        return focal_map

    def _set_camera_intrinsic_matrix(self, width: int, height: int) -> None:
        """
        runs once when normalize_image called
        intrinsic matrix ist in unserem fall immer:
        [[focal_x, 0.0, optical_center_x], [0.0, focal_y, optical_center_x], [0.0, 0.0, 1.0]]
        focal_x = focal_y = kommt aus der Config und ist in der Regel 1400 (wir nutzen der einfachheit 1000)
        opical_center_x = width/2
        opical_center_y = height/2
        könnte aber theoretisch auch verschoben sein.
        Wir nehmen an das unsere Kameras ihre Optische Mitte auch in der Mitte haben.
        """
        self.camera_intrinsic_matrix = array(
            [
                [self.focal, 0, width / 2],
                [0, self.focal, height / 2],
                [0, 0, 1],
            ],
            dtype=numpy.float32,
        )

    def _set_distortions_maps(self, width: int, height: int) -> None:
        """runs once when normalize_image called"""
        self.map_x, self.map_y = initUndistortRectifyMap(
            self.camera_intrinsic_matrix,
            self.distortion_coefficients,
            eye(3),
            self.camera_intrinsic_matrix,
            (width, height),
            CV_16SC2,
        )

    def check_init(self, width: int, height: int) -> None:
        if self.camera_intrinsic_matrix is None:
            self._set_camera_intrinsic_matrix(width, height)
        if not self.map_init:
            self._set_distortions_maps(width, height)
            self.map_init = True

    def normalize_enriched_frame(self, frame: EnrichedFrame) -> Image:
        """corrects the focal distortion"""
        self.check_init(frame.width, frame.height)
        return remap(  # type: ignore[no-any-return]
            frame.frame,
            self.map_x,
            self.map_y,
            interpolation=INTER_LINEAR,
            borderMode=BORDER_CONSTANT,
        )

    def normalize_image(self, image: Image) -> Image:
        """corrects the focal distortion"""
        image_height, image_width = image.shape[:2]
        self.check_init(image_width, image_height)
        return remap(  # type: ignore[no-any-return]
            image,
            self.map_x,
            self.map_y,
            interpolation=INTER_LINEAR,
            borderMode=BORDER_CONSTANT,
        )
