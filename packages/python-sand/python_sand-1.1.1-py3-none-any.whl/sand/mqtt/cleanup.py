from __future__ import annotations

from time import sleep

from paho.mqtt.client import Client, MQTTMessage, MQTTv5

from sand.logger import Logger

_LOG: Logger
_RETAINED_TOPIC_COUNTER = 0


def _on_message(client: Client, _: None, msg: MQTTMessage) -> None:
    # pylint: disable=global-statement
    global _RETAINED_TOPIC_COUNTER

    if msg.retain:
        _LOG.i(f"retained topic found: {msg.topic}", "_on_message")

        client.publish(msg.topic, payload=None, retain=True)
        _RETAINED_TOPIC_COUNTER += 1


def reset_broker(host: str, sleep_time: float = 1.0) -> None:
    # pylint: disable=global-statement
    global _LOG

    _LOG = Logger("MQTT Cleanup")

    client = Client(client_id="mqtt_cleanup", protocol=MQTTv5)

    client.on_message = _on_message

    _LOG.i("Starting MQTT Cleanup", "reset_broker")
    client.connect(host)
    client.subscribe("#")
    client.loop_start()
    sleep(sleep_time)
    client.loop_stop()
    client.disconnect()

    _LOG.i(f"Cleaned {_RETAINED_TOPIC_COUNTER} retained topics", "reset_broker")
