from __future__ import annotations

import pickle
import uuid
from functools import partial
from threading import Event
from typing import Any, Callable

from overrides import overrides
from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from sand.config import CommunicationConfig
from sand.datatypes import Topic
from sand.datatypes.datapoint import ReconnectMetric
from sand.interfaces.shutdown import ShutdownAble
from sand.logger import Logger

from .mqtt_util import get_client_with_reconnect


class Communicator(ShutdownAble):
    """Abstraction layer to make MQTT communication easier.

    For debugging it could sometimes help to see the direct logs of the client itself.
    To enable them you can use:
        self.client.on_log = print
    """

    raw_datatypes = {"int": int, "float": float, "str": str, "bool": bool}

    def __init__(
        self,
        config: CommunicationConfig,
        client_id: str | None = None,
    ) -> None:
        ShutdownAble.__init__(self, config)
        self.__config = config

        self.__communication_log = Logger(f"com_{self.__class__.__name__}")

        self.__initial_connect = True
        self.__connected_event = Event()

        self.client: Client | None = None

        if self.__config.use_mqtt:
            self.client = get_client_with_reconnect(
                client_id=f"com_{self.__class__.__name__}_{uuid.uuid4()}"
                if client_id is None
                else client_id,
                logger=self.__communication_log,
            )
            self.client.on_connect = self.__on_connect

    def __publish_reconnect(self) -> None:
        if not self.__initial_connect:
            self.__pure_publish(
                payload=ReconnectMetric(self.__class__.__name__).get_point(),
                topic=f"{self.__class__.__name__}/Communicator/metric/data",
            )

    def __on_connect(
        self,
        _: Client,
        __: None,
        ___: dict[str, Any],
        reason_code: int,
        ____: Properties,
    ) -> None:
        # The value of rc indicates success or not:
        #   0: Connection successful
        #   1: Connection refused - incorrect protocol version
        #   2: Connection refused - invalid client identifier
        #   3: Connection refused - server unavailable
        #   4: Connection refused - bad username or password
        #   5: Connection refused - not authorised
        self.__communication_log.w(
            f"{self.__class__.__name__=} rc={reason_code!s}", "__on_connect"
        )
        self.__connected_event.set()

    def __connect(self) -> None:
        if self.client is not None and not self.client.is_connected():
            self.__connected_event.clear()
            self.__connect_client()
            self.client.loop_start()
            self.__connected_event.wait()

            self.__publish_reconnect()
            self.__initial_connect = False

    def __connect_client(self) -> None:
        assert self.client is not None

        if self.__initial_connect:
            result = self.client.connect(self.__config.host)
        else:
            result = self.client.reconnect()
        self.__communication_log.w(
            f"name: {self.__class__.__name__} | connection: {self.__initial_connect} | result: {result}",
            "__connect_client",
        )

    @staticmethod
    def __unpack_property__(search: str, properties: Properties) -> str:
        if properties.UserProperty:
            for prop in properties.UserProperty:
                if prop[0] == search:
                    return str(prop[1])
        return ""

    def __callback(
        self,
        _: Client,
        __: None,
        msg: MQTTMessage,
        callback: Callable[[Topic, Any], None],
    ) -> None:
        try:
            datatype = Communicator.__unpack_property__("datatype", msg.properties)
            if datatype in Communicator.raw_datatypes:
                callback(msg.topic, Communicator.raw_datatypes[datatype](msg.payload))
            else:
                callback(msg.topic, pickle.loads(msg.payload))
        # Expected ones are EOFError, UnpicklingError, but also whatever else
        # pylint: disable=broad-except
        except Exception:
            self.__communication_log.exception(
                f"Exception in callback: topic: {msg.topic} | properties: {msg.properties}",
                "__callback",
            )

    def subscribe_topic(
        self,
        topic: Topic,
        callback: Callable[[Topic, Any], None],
    ) -> None:
        if self.client is None:
            self.__communication_log.i(
                "No client initialized, subscription will not take place",
                "subscribe_topic",
            )
            return

        self.__connect()

        curried_callback = partial(self.__callback, callback=callback)
        curried_callback.__name__ = topic  # type: ignore[attr-defined]
        self.client.message_callback_add(
            topic,
            curried_callback,
        )
        self.client.subscribe(topic, qos=1)

    def publish(
        self, payload: Any, topic: str, retain: bool = False, qos: int = 0
    ) -> None:
        if self.client is None:
            self.__communication_log.d(
                "No client initialized, cannot publish",
                "subscribe_topic",
            )
            return

        self.__connect()

        self.__pure_publish(payload, topic, retain, qos)

    def __pure_publish(
        self, payload: Any, topic: str, retain: bool = False, qos: int = 0
    ) -> None:
        assert self.client is not None

        payload_type = str(type(payload))
        publish_properties = Properties(PacketTypes.PUBLISH)
        publish_properties.UserProperty = ("datatype", payload_type)

        self.client.publish(
            topic=topic,
            payload=payload
            if payload_type in Communicator.raw_datatypes
            else pickle.dumps(payload),
            retain=retain,
            qos=qos,
            properties=publish_properties,
        )

    @overrides
    def shutdown(self) -> None:
        if self.client is not None:
            self.__connected_event.set()
            self.client.loop_stop()
            self.client.disconnect()

        ShutdownAble.shutdown(self)
