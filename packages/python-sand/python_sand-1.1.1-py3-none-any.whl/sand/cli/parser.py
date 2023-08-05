from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

from sand.config.config import CommunicationConfig
from sand.logger import initialize_logger
from sand.mqtt.cleanup import reset_broker  # allowed

from .arguments import Arguments

_DEFAULT_CONFIG_DIR = "config/automodal-configs/"


def _get_config_path(parsed: Path | None) -> tuple[int, Path | None]:
    if parsed is not None and not parsed.exists():
        print(  # allowed
            f"Your given config does not exist, path: {parsed} | "
            f"absolute: {parsed.absolute()}",
            file=sys.stderr,
        )
        return -1, None

    for index, config_path in enumerate(
        [
            parsed,
            Path(f"../{_DEFAULT_CONFIG_DIR}/sand/system/sand_config.yaml"),
            Path(f"{_DEFAULT_CONFIG_DIR}/sand/system/sand_config.yaml"),
        ]
    ):
        if config_path is not None and config_path.exists():
            return index, config_path

    return -1, None


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="System to record the data on a trimodal crane")

    parser.add_argument(
        "--config",
        type=str,
        help="Path to the configuration file, default is either "
        f"'../{_DEFAULT_CONFIG_DIR}/sand/system/sand_config.yaml' or "
        f"'{_DEFAULT_CONFIG_DIR}/sand/system/sand_config.yaml'"
        "depending on where the script is called from",
    )
    parser.add_argument(
        "--playback", type=str, help="Path to the segment you want to play back"
    )
    parser.add_argument(
        "--log",
        type=str,
        default="DEBUG",
        help="Set the loglevel for the stdout-Logging, see '--general-log' for other options; "
        "values are: WARNING, INFO, DEBUG",
    )
    parser.add_argument(
        "--general-log",
        type=str,
        default="DEBUG",
        help="Set the GENERAL loglevel for all file handlers, this should be DEBUG, "
        "to have the full log in the logfile, so use with caution; values are: WARNING, INFO, DEBUG",
    )
    parser.add_argument(
        "--logfile",
        type=str,
        default="crane_system.log",
        help="How the logfile should be named",
    )
    parser.add_argument(
        "--log-path",
        type=str,
        help="To set the path to the logging file, default is either '../logs' or 'logs' "
        "depending on where the script is called from, similar to '--config'",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Just start everything once and then die, should help to locate missing packages and start errors",
    )
    parser.add_argument(
        "--no-mosquitto-clean",
        action="store_true",
        help="If you don't want to get your retained messages cleaned and basically your mosquitto reset "
        "or don't have access to the mosquitto clients.",
    )

    parser.add_argument(
        "--gpus",
        type=int,
        default=0,
        help="How many GPUs should be used for this run, 0=disable gpu "
        "specification, meaning you can still use a gpu but you are bound by "
        "what your framework recognizes. If >=1 your cameras will be split onto "
        "different processes each with their own GPU set via the "
        "'CUDA_VISIBLE_DEVICES' environment variable.",
    )

    parser.add_argument(
        "--ignore-on-shutdown",
        action="store_true",
        help="DEVELOPMENT_OPTION: This should not be used in any production "
        "environment. It causes the main process to immediately shutdown "
        "(on the second Ctrl+C that you send), without waiting for the services "
        "to end their threads. This _will_ corrupt recordings and other data, "
        "but can be useful if you develop on the system.",
    )

    parser.add_argument(
        "--custom-start-module",
        type=str,
        default="",
        help="You want to use our cli interface but define your own system? "
        "Sure, tell us which module we should import and make sure that the "
        "imported thing provides the correct API.\n"
        "Disclaimer: This technically is able to execute arbitrary code, "
        "so be careful when using it",
    )

    return parser


def _check_dir(possible_path: str | None) -> Path | None:
    result: Path | None = None

    if possible_path is not None:
        result = Path(possible_path)

        if not Path(possible_path).is_dir():
            raise NotADirectoryError(
                f"Playback doesn't exist or is not a directory: {possible_path!r}"
            )

    return result


def parse() -> Arguments:
    parser = get_parser()
    args = parser.parse_args()

    config_index, config_path = _get_config_path(
        None if args.config is None else Path(args.config)
    )

    if config_path is None:
        print()  # allowed
        parser.print_help()
        print()  # allowed
        raise FileNotFoundError(
            f"No config found on path: {args.config!r} or on the default locations"
        )

    playback = _check_dir(args.playback)

    log, logger_listener = initialize_logger(
        logfile=args.logfile,
        log_path_str=args.log_path,
        config_index=config_index,
        stdout_level=args.log,
        mqtt_server="127.0.0.1",
        use_mqtt=True,
    )

    if not args.no_mosquitto_clean:
        reset_broker(CommunicationConfig().host)
    else:
        log.i("No cleanup of mosquitto was done", "parse")

    arguments = Arguments(
        config_path,
        logger_listener,
        playback,
        args.check,
        args.gpus,
        args.ignore_on_shutdown,
        args.custom_start_module,
    )
    log.d(f"CLI Arguments: {arguments=}", "parse")

    log.i(f"Using config: {config_path}", "parse")
    return arguments
