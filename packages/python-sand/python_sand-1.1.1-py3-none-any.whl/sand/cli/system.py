from __future__ import annotations

from importlib import import_module

from .parser import parse
from .starter import SandStarter


def _get_starter(possible_module: str) -> SandStarter:
    if possible_module == "":
        return SandStarter()

    try:
        starter = import_module(possible_module).CustomSandStarter()
    except ImportError as import_error:
        raise ImportError(
            f"Could not import custom start module: {possible_module!r}"
        ) from import_error

    if not isinstance(starter, SandStarter):
        raise ImportError("Imported object doesn't fullfill the SandStarter interface.")

    return starter


def run() -> None:
    args = parse()

    _get_starter(args.custom_start_module).start_system(args)
