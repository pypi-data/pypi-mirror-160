from __future__ import annotations

from numpy import clip, zeros

from sand.config import SensorFusionConfig
from sand.datatypes.types import HeatMapArray, Point


class HeatMap:
    def __init__(self, config: SensorFusionConfig):
        self.config = config
        self.current_state = self.get_empty_heat_map()
        self._cool_down_map = self.get_empty_heat_map() + self.config.cool_down_factor
        self._heat_up_map = self.get_empty_heat_map() + self.config.heat_up_factor
        self._calculation_state = self.get_empty_heat_map()

    def calc(self) -> None:
        self.current_state -= (self._calculation_state == 0) * self._cool_down_map
        self.current_state += (self._calculation_state != 0) * self._heat_up_map
        clip(self.current_state, 0, 25)
        self._calculation_state = self.get_empty_heat_map()

    # noinspection PyTypeChecker
    def get_empty_heat_map(self) -> HeatMapArray:
        return zeros(
            (
                int(
                    self.config.map_height
                    * self.config.scale
                    / self.config.heat_map_cluster_size
                ),
                int(
                    self.config.map_width
                    * self.config.scale
                    / self.config.heat_map_cluster_size
                ),
            ),
            dtype=int,
        )

    def add_point_to_heat_map(self, point: Point) -> None:
        """
        Raises:
            IndexError:
                in case of index access in heat_map fails
        """
        if (
            0 <= point.y < self.config.map_height * self.config.scale
            and 0 <= point.x < self.config.map_width * self.config.scale
        ):
            cluster_size = self.config.heat_map_cluster_size
            self._calculation_state[int(point.y / cluster_size)][
                int(point.x / cluster_size)
            ] += 1
