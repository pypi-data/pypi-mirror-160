from __future__ import annotations

from typing import TypeVar

from overrides import EnforceOverrides


class RegisterAble(EnforceOverrides):
    def __init__(self) -> None:
        _nodes.append(self)


_nodes: list[RegisterAble] = []
T = TypeVar("T", bound=RegisterAble)


def get_node_count() -> int:
    return len(_nodes)


def get_nodes(node_type: type[T]) -> list[T]:
    return list(filter(lambda x: isinstance(x, node_type), _nodes))  # type: ignore[arg-type]


def get_singleton_node(node_type: type[T]) -> T:
    nodes: list[T] = list(filter(lambda x: isinstance(x, node_type), _nodes))  # type: ignore[arg-type]

    if len(nodes) == 1:
        return nodes[0]

    raise ValueError(
        f"ERROR: No single node available for type: {node_type}, available nodes: {nodes}"
    )
