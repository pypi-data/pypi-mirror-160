from __future__ import annotations

from functools import partial

from paho.mqtt.client import MQTT_ERR_SUCCESS, Client, MQTTv5
from paho.mqtt.properties import Properties

from sand.logger import Logger


def _on_disconnect(
    client: Client,
    __: None,
    reason_code: int,
    ___: Properties,
    logger: Logger | None = None,
) -> None:
    print(  # allowed
        f"reason_code: {reason_code} | "  # pylint: disable=protected-access
        f"MQTT_ERR_SUCCESS: {MQTT_ERR_SUCCESS} | "
        f"client_id: {client._client_id}"
    )
    if reason_code != MQTT_ERR_SUCCESS:
        if logger is not None:
            logger.w(
                f"communicator client: '{client._client_id}' "  # pylint: disable=protected-access
                "got disconnected, retrying...",
                "__on_disconnect",
            )

        # should restore subscriptions automatically, messages are not resent though
        client.reconnect()


def get_client_with_reconnect(
    client_id: str = "",
    protocol: int = MQTTv5,
    logger: Logger | None = None,
) -> Client:
    client = Client(client_id=client_id, protocol=protocol)
    client.on_disconnect = partial(_on_disconnect, logger=logger)
    return client
