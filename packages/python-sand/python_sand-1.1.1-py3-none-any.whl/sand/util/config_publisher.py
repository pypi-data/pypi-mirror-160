from __future__ import annotations

from typing import Any

from config_builder import BaseConfigClass
from related import TypedSequence

from sand.config.config import SandConfig
from sand.interfaces.communication import Communicator
from sand.interfaces.config import ConfigurationManager

__DEVICE_PLACEHOLDER = "DEVICE_PLACE_HOLDER"


def _set_device(topic: str, device: str) -> str:
    return topic.replace(__DEVICE_PLACEHOLDER, device)


def _publish_final_element(
    communicator: Communicator, topic_prefix: str, subitem: Any
) -> None:
    communicator.publish(subitem, _set_device(topic_prefix, "all"), retain=True)


def _publish_subitem(
    communicator: Communicator, topic_prefix: str, subitem: Any
) -> None:
    if issubclass(subitem.__class__, BaseConfigClass):
        for key, item in subitem.__dict__.items():
            _publish_subitem(communicator, f"{topic_prefix}/{key}", item)
    elif issubclass(subitem.__class__, (list, TypedSequence)):
        try:
            for item in subitem:
                _publish_subitem(
                    communicator, _set_device(topic_prefix, item.name), item
                )
        except AttributeError:
            # item has no 'name' therefore the list is the final element
            _publish_final_element(communicator, topic_prefix, subitem)
    else:
        _publish_final_element(communicator, topic_prefix, subitem)


def publish_config(global_config: SandConfig) -> None:
    _topic_prefix = f"{ConfigurationManager.__name__}/{__DEVICE_PLACEHOLDER}/data"
    communicator = Communicator(
        global_config.communication,
        client_id="config_publisher",
    )

    for key, item in global_config.__dict__.items():
        _publish_subitem(communicator, f"{_topic_prefix}/{key}", item)

    communicator.self_destroy()
