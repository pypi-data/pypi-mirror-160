from __future__ import annotations

import re
from logging import DEBUG, Formatter, Handler, LogRecord, RootLogger, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from sys import stdout
from time import sleep
from uuid import uuid4

from overrides import overrides
from paho.mqtt.client import MQTT_ERR_SUCCESS, Client, MQTTMessage, MQTTv5
from paho.mqtt.properties import Properties


def __on_disconnect(
    client: Client,
    __: None,
    reason_code: int,
    ___: Properties,
) -> None:
    if reason_code != MQTT_ERR_SUCCESS:
        # should restore subscriptions automatically, messages are not resent though
        client.reconnect()


def _get_client_with_reconnect(
    client_id: str = "",
    protocol: int = MQTTv5,
) -> Client:
    client = Client(client_id=client_id, protocol=protocol)
    client.on_disconnect = __on_disconnect
    return client


class MQTTLogger(Handler):
    def __init__(self, host: str, level: str = "DEBUG") -> None:
        Handler.__init__(self, level)

        self.__host = host

        self.__logger_client = _get_client_with_reconnect(client_id=f"logger_{uuid4()}")

    @overrides
    def emit(self, record: LogRecord) -> None:
        if not self.__logger_client.is_connected():
            self.__logger_client.connect(self.__host)

        msg = self.format(record)

        topic_suffix = "root" if record.name == "" else record.name
        self.__logger_client.publish(
            topic=f"{MQTTLogger.__name__}/{topic_suffix}/data/log",
            payload=msg,
        )


class MQTTLoggerListener:
    def __init__(self, host: str, log_file: Path, console_level: str = "DEBUG") -> None:
        self.__log = self.__create_logger(log_file, console_level)

        self.__logger_client = _get_client_with_reconnect(
            client_id=f"logger_listener_{uuid4()}"
        )
        self.__logger_client.message_callback_add(
            f"{MQTTLogger.__name__}/#", self.__on_log_message
        )
        self.__logger_client.connect(host)
        self.__logger_client.subscribe(f"{MQTTLogger.__name__}/#")

        self.__log_banner("LOG RECORDING STARTED")

        self.__logger_client.loop_start()
        # the sleep is required or else the mqtt loop thread is not
        # initialised at returning from logger creation
        # see also:
        # https://github.com/eclipse/paho.mqtt.python/issues/345
        sleep(0.3)

    @staticmethod
    def __create_logger(log_file: Path, console_level: str = "DEBUG") -> RootLogger:
        log = RootLogger(DEBUG)

        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="h",
            interval=6,
        )
        file_handler.suffix = "%Y-%m-%d_%H.log"
        file_handler.extMatch = re.compile(
            r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?\.log$", re.ASCII
        )
        file_handler.setLevel(DEBUG)

        stream_handler = StreamHandler(stream=stdout)
        stream_handler.setLevel(console_level)

        formatter = Formatter("%(message)s")
        file_handler.formatter = formatter
        stream_handler.formatter = formatter

        log.addHandler(file_handler)
        log.addHandler(stream_handler)

        return log

    def __log_banner(self, purpose: str) -> None:
        self.__log.info(
            "############################################################################"
        )
        self.__log.info("# %s", purpose)
        self.__log.info(
            "############################################################################"
        )

    def shutdown(self) -> None:
        self.__logger_client.loop_stop()
        self.__logger_client.disconnect()

        self.__log_banner("LOG RECORDING FINISHED")

    def __on_log_message(self, _: Client, __: None, msg: MQTTMessage) -> None:
        self.__log.info(msg.payload.decode())
