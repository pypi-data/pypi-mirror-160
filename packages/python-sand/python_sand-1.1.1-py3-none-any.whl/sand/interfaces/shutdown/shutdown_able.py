from __future__ import annotations

from abc import abstractmethod
from threading import Event
from uuid import uuid4

from overrides import EnforceOverrides
from paho.mqtt.client import MQTT_ERR_SUCCESS, Client, MQTTv5

from sand.config import CommunicationConfig
from sand.registry import RegisterAble


class ShutdownAble(RegisterAble, EnforceOverrides):
    def __init__(
        self,
        config: CommunicationConfig,
        override_client: Client | None = None,
    ) -> None:
        RegisterAble.__init__(self)

        self.shutdown_event = Event()

        self.__uuid = uuid4()
        self.__shutdown_client: Client | None = self.__create_mqtt_client(
            config,
            override_client,
        )

    def __create_mqtt_client(
        self,
        config: CommunicationConfig,
        override_client: Client | None = None,
    ) -> Client | None:
        if not config.use_mqtt:
            return None

        if override_client is not None:
            client = override_client
        else:
            client = Client(
                client_id=f"SA/{self.__class__.__name__}/{self.__uuid}",
                protocol=MQTTv5,
            )

        self.__setup_shutdown_client(client, config)

        return client

    def __setup_shutdown_client(
        self, client: Client, config: CommunicationConfig
    ) -> None:
        client.will_set(
            topic=self._get_finished_topic(),
            payload=self._get_payload(),
            retain=False,
            qos=1,
        )
        client.on_disconnect = lambda _, __, reason_code, ___: self.self_destroy(
            disconnect=reason_code != MQTT_ERR_SUCCESS
        )
        client.connect(config.host)
        client.publish(
            topic=self._get_register_topic(),
            payload=self._get_payload(),
            retain=False,
            qos=1,
        )
        client.message_callback_add(
            ShutdownAble.get_shutdown_topic(),
            lambda *_, **__: self.self_destroy(),
        )
        client.subscribe(ShutdownAble.get_shutdown_topic(), qos=1)
        client.loop_start()

    def self_destroy(self, disconnect: bool = False) -> None:
        if self.shutdown_event.is_set():
            print(  # allowed, as clients are possibly disconnected and no log available
                f"Got shutdown twice, preventing: {self.__class__.__name__}_{self.__uuid}"
            )
            return

        if disconnect and self.__shutdown_client is not None:
            self.__shutdown_client.publish(
                f"MQTTLogger/{self.__class__.__name__}_{self.__uuid}/data/log",
                payload=f"WARNING: Got disconnected from broker: {self.__class__.__name__}_{self.__uuid}",
                qos=1,
            )
            print(  # allowed, as clients are possibly disconnected and no log available
                f"Got disconnected: {self.__class__.__name__}_{self.__uuid}"
            )

        self.shutdown_event.set()

        self.shutdown()

        self._report_finished_shutdown()

        if self.__shutdown_client is not None:
            self.__shutdown_client.loop_stop()
            self.__shutdown_client.disconnect()

    def _report_finished_shutdown(self) -> None:
        if self.__shutdown_client is not None:
            self.__shutdown_client.publish(
                topic=self._get_finished_topic(),
                payload=self._get_payload(),
                retain=False,
                qos=1,
            )

    def _get_payload(self) -> str:
        return f"{self.__class__.__name__}|{self.__uuid}"

    def _get_register_topic(self) -> str:
        return f"{ShutdownAble.__name__}/{self.__uuid}/command/register_shutdown"

    def _get_finished_topic(self) -> str:
        return f"{ShutdownAble.__name__}/{self.__uuid}/command/finished_shutdown"

    @staticmethod
    def get_shutdown_topic() -> str:
        return f"{ShutdownAble.__name__}/all/command/shutdown"

    @abstractmethod
    def shutdown(self) -> None:
        """
        Method to get notified of a shutdown, making it able to clean up before terminating.
        The whole cleanup should be implemented synchronously in this method. A return signals
        a successful cleanup. Raised errors will be ignored.
        """
