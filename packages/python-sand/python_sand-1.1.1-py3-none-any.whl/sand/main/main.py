from __future__ import annotations

from signal import SIGTERM, signal
from threading import Event, Thread
from time import sleep
from typing import Any

from paho.mqtt.client import Client, MQTTMessage, topic_matches_sub

from sand.config import CommunicationConfig
from sand.interfaces.communication import get_client_with_reconnect
from sand.interfaces.shutdown import ShutdownAble
from sand.logger import Logger, MQTTLoggerListener
from sand.util.time import now


class Main:
    __REGISTER_TOPIC = "+/+/command/register_shutdown"
    __REPORT_TOPIC = "+/+/command/finished_shutdown"

    def __init__(
        self,
        logger_listener: MQTTLoggerListener | None = None,
        sleep_time: int = 3600,
        ignore_on_shutdown: bool = False,
    ) -> None:
        self.log = Logger(self.__class__.__name__)
        self.sleep_time = sleep_time
        self.ignore_on_shutdown = ignore_on_shutdown

        signal(SIGTERM, self._handle)

        self.logger_listener = logger_listener

        self.__main_client = get_client_with_reconnect(client_id="main")
        self.__main_client.on_message = self._change_shutdown_able
        self.__main_client.connect(CommunicationConfig().host)
        self.__main_client.subscribe(Main.__REGISTER_TOPIC, qos=1)
        self.__main_client.subscribe(Main.__REPORT_TOPIC, qos=1)

        self._shutdown_ables: set[str] = set()
        self._shutdown_in_progress = False
        self._shutdown_event = Event()
        self._all_clients_shutdown = Event()
        self.__main_client.loop_start()

    def _change_shutdown_able(self, _: Client, __: None, msg: MQTTMessage) -> None:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        is_register = topic_matches_sub(Main.__REGISTER_TOPIC, topic)

        self.log.i(
            f"Change in shutdown_ables: is_register: {is_register} | "
            f"topic: {topic} | payload: {payload} | "
            f"current count: {len(self._shutdown_ables)}",
            "_change_shutdown_able",
        )

        if is_register:
            if payload in self._shutdown_ables:
                self.log.exception(
                    "Received register shutdown with already recognized payload: "
                    f"is_register: {is_register} | payload: {payload} | topic: {topic} | "
                    f"shutdown_ables: {self._shutdown_ables}",
                    "_change_shutdown_able",
                )
            else:
                self._shutdown_ables.add(payload)
        else:
            try:
                self._shutdown_ables.remove(payload)
            except KeyError:
                self.log.exception(
                    "Received finished shutdown with unrecognized payload: "
                    f"is_register: {is_register} | payload: {payload} | topic: {topic} | "
                    f"shutdown_ables: {self._shutdown_ables}",
                    "_change_shutdown_able",
                )

        if self._shutdown_in_progress and len(self._shutdown_ables) == 0:
            self._all_clients_shutdown.set()

    def spin(self, check: bool = False) -> None:
        fct = "spin"
        while not self._shutdown_event.is_set():
            if check:
                self.log.w(
                    "Only a check run, executing shutdown, waiting shortly to give other time",
                    fct,
                )
                self._shutdown_event.wait(10)
                self.log.d(
                    f"All registered shutdown ables: {len(self._shutdown_ables)} | {self._shutdown_ables}",
                    fct,
                )
                self._handle(6660, "")
                continue

            try:
                self._shutdown_event.wait(self.sleep_time)
            except KeyboardInterrupt:
                self.log.d("Caught KeyboardInterrupt, shutting down...", fct)
                self._handle(666, "")

        self.log.w(
            "############################################################################",
            fct,
        )
        self.log.w("# SYSTEM SHUTDOWN", fct)
        self.log.w(
            "############################################################################",
            fct,
        )
        # was 1 but is 0.1 also enough?!
        sleep(0.1)
        if self.logger_listener is not None:
            self.logger_listener.shutdown()

    def _publish_shutdown(self) -> None:
        while not self._all_clients_shutdown.is_set():
            self.__main_client.publish(
                payload=f"{now()}",
                topic=ShutdownAble.get_shutdown_topic(),
                retain=True,
                qos=1,
            )
            self._all_clients_shutdown.wait(1)

    def _handle(self, signum: int, _: Any) -> None:
        fct = "_handle"
        self.log.w(f"Received signal: {signum} | now: {now()}", fct)
        while not self._shutdown_event.is_set():
            try:
                self._shutdown_in_progress = True

                shutdown_publisher = Thread(
                    target=self._publish_shutdown, name="ShutdownPublisher"
                )
                shutdown_publisher.start()

                if len(self._shutdown_ables) != 0:
                    self._all_clients_shutdown.wait(30)
                    if not self._all_clients_shutdown.is_set():
                        self.log.w(
                            "Not all registered clients shutdown successfully, "
                            f"remaining: {len(self._shutdown_ables)} | {self._shutdown_ables}",
                            fct,
                        )
                    else:
                        self.log.i("Successful shutdown of everything", fct)

                self.log.i("Shutting down Main", fct)
                self._all_clients_shutdown.set()
                shutdown_publisher.join()
                self.log.i("Shutdown Event sender is done", fct)
                self._shutdown_event.set()
            except KeyboardInterrupt:
                self.log.d(
                    "Recognized KeyboardInterrupt while shutting down, preventing...",
                    fct,
                )
                self.log.w(
                    f"Currently waiting on: {len(self._shutdown_ables)} | {self._shutdown_ables}",
                    fct,
                )
                if self.ignore_on_shutdown:
                    self.log.e("We are not waiting, shutdown immediately...", fct)
                    self._all_clients_shutdown.set()
                    self._shutdown_event.set()
                    break
