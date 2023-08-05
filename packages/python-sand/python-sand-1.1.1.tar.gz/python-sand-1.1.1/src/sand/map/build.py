from __future__ import annotations

from copy import copy

import cv2

from sand.datatypes import Dimensions, EnrichedFrame
from sand.datatypes.aerialmap import AerialMap
from sand.util.image import crop_image_on_map


def build_map(
    images: dict[str, EnrichedFrame],
    map_id: int,
    map_width: int,
    map_height: int,
    scale: float = 0.1,
) -> AerialMap:
    """
    takes all frames of the moment and throws it in a new map object.
    than build a new representation of images, detections and las0rs
    We throw an copy of the moment dictonary in the new CraneMap Obj.
    Its like a moment recording with the correct pointer to the original Frame Obj.
    """
    images_copy = copy(images)
    terminal_map = AerialMap(
        images_copy,
        Dimensions(map_width, map_height),
        scale,
        map_id,
    )

    # add images
    for camera_name, image in images_copy.items():
        if image.mapped_frame is not None:
            height = int(map_height * scale)
            width = int(map_width * scale)
            resized_image = cv2.resize(
                image.mapped_frame,
                (
                    width,
                    height,
                ),
            )
            cropped_image = crop_image_on_map(
                image=resized_image,
                name=camera_name,
                target_width=width,
                target_height=height,
            )
            terminal_map.add_frame(cropped_image)

    return terminal_map
