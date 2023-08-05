from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any, Generic, Pattern, TypeVar

from config_builder import BaseConfigClass
from related import TypedSequence

from sand.config import CameraConfig, LidarConfig, SandConfig
from sand.datatypes import Topic
from sand.interfaces.communication import Communicator
from sand.logger import Logger

T = TypeVar("T")
LidarOrCameraConfig = TypeVar("LidarOrCameraConfig", CameraConfig, LidarConfig)


def find_config(
    device_name: str,
    config_list: list[LidarOrCameraConfig],
) -> LidarOrCameraConfig | None:
    """Method to find specific camera or lidar config from list based on the device name."""
    for config in config_list:
        if config.name == device_name:
            return config
    return None


class ConfigurationManager(Generic[T]):
    def __init__(
        self,
        communicator: Communicator,
        global_config: SandConfig,
        update_pattern: str = r".*",
    ) -> None:
        """
        Args:
            communicator: which communicator to use
            global_config: the initial configuration for a faster startup
            update_pattern: full-regex pattern to be notified when
                updates to this config happens
        """
        self.communicator = communicator
        self._global_config = global_config
        self.__log = Logger(f"cm_{self.communicator.__class__.__name__}")
        self.__update_topic_regex: Pattern[str] = re.compile(update_pattern)

        self.communicator.subscribe_topic(
            f"{ConfigurationManager.__name__}/+/data/#", self._set_new_config
        )

    def _set_new_config(self, topic: Topic, new_value: Any) -> None:
        topic_splits = topic.split("/")

        is_set_successful = False
        device = topic_splits[1]
        intermediary: Any = self._global_config
        for path_element in topic_splits[3:]:
            element = getattr(intermediary, path_element)
            if issubclass(element.__class__, BaseConfigClass):
                intermediary = element
            elif issubclass(element.__class__, (list, TypedSequence)):
                try:
                    intermediary = find_config(device, element)
                    assert intermediary is not None
                except AttributeError:
                    # element has no '.name' therefore it's probably a leaf item
                    is_set_successful = True
                    self._update_attribute(topic, intermediary, path_element, new_value)
            else:
                is_set_successful = True
                self._update_attribute(topic, intermediary, path_element, new_value)

        if not is_set_successful:
            self.__log.e(
                f"Did not find new value to set: topic: {topic} | new_value: {new_value}",
                "_set_new_config",
            )

    def _update_attribute(
        self, topic: str, leaf: Any, attribute: str, new_value: Any
    ) -> None:
        element = getattr(leaf, attribute)
        if element == new_value:
            # no update
            return

        setattr(leaf, attribute, new_value)

        if self.__update_topic_regex.match(topic) is not None:
            self.config_has_updated()

    def config_has_updated(self) -> None:
        """Callback function that gets executed when an update to the config
        has happened and the regex in {self.__update_topic_regex} matches the
        changed topic.

        This method is intended to be used in conjunction with setting the
        {update_pattern} to a regex that matches only sub-updates. Otherwise,
        there are potentially a lot of false-positive updates.
        """

    @property
    def config(self) -> T:
        return self.select_config(self._global_config)

    @abstractmethod
    def select_config(self, global_config: SandConfig) -> T:
        """Function which selects your sub-config from the global SANDConfig.

        Obviously should be fast, as probably called often. If your module needs
        multiple configuration objects the recommendation would be to make them
        a NamedTuple and create this tuple in here.
        """
