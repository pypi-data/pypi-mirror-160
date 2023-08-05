from __future__ import annotations

from logging import WARNING, getLogger
from logging.config import dictConfig
from pathlib import Path

from .logger import Logger
from .mqtt_logger import MQTTLoggerListener


def _get_log_path(index: int, parsed: str | None) -> Path:
    if parsed is not None:
        return Path(parsed)

    paths = [Path(""), Path("../logs"), Path("logs")]

    if 0 < index < len(paths):
        paths[index].mkdir(exist_ok=True)
        return paths[index]

    # if invalid value or 0 is given, return empty default
    return paths[0]


def initialize_logger(  # pylint: disable=too-many-arguments
    logfile: Path,
    log_path_str: str | None,
    config_index: int,
    stdout_level: str | None,
    mqtt_server: str = "127.0.0.1",
    use_mqtt: bool = True,
) -> tuple[Logger, MQTTLoggerListener | None]:
    log_path = _get_log_path(config_index, log_path_str)
    getLogger("matplotlib").setLevel(WARNING)
    logger_listener = None
    if use_mqtt:
        dictConfig(Logger.get_mqtt_handler_config())
        logger_listener = MQTTLoggerListener(
            mqtt_server, log_file=Path(log_path, logfile)
        )
    else:
        dictConfig(
            Logger.get_stdout_handler_config(
                stdout_level=stdout_level if stdout_level is not None else "INFO"
            )
        )

    log = Logger("system_parse")

    log.i(
        "############################################################################",
        "parse",
    )
    log.i("# SYSTEM START", "parse")
    log.i(
        "############################################################################",
        "parse",
    )
    return log, logger_listener
