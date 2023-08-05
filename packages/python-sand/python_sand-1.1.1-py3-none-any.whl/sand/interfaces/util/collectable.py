from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

from overrides import EnforceOverrides

T = TypeVar("T")


class CollectAble(EnforceOverrides, Generic[T]):
    @abstractmethod
    def subscribe(self, subscriber: T) -> None:
        """
        Subscriber mechanic where the subscriber gets notified of something that is collected.

        Generally recommended in some kind of __init__ of the Subscriber so it should be:

        collectable.subscribe(self, scale=42)

        Also use the generic CollectAble only if you know what you are doing. Our recommendation is to use the more
        specific CollectAble-Variants with more specific typing hints.
        """
