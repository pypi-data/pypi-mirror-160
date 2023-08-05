from __future__ import annotations

from time import time

from sand.datatypes.delta import Delta
from sand.interfaces.communication import Communicator


# pylint: disable=too-many-arguments
class DeltaHelper:
    def __init__(
        self,
        communicator: Communicator,
        device_name: str,
        data_id: int,
        source: list[str],
        data_type: str = "frame",
    ) -> None:
        self.communicator = communicator
        self.module_name = communicator.__class__.__name__
        self.device_name = device_name
        self.delta = Delta(
            id=data_id,
            type=data_type,
            source=",".join(source),
            device_name=device_name,
            start=time(),
            end=time(),
        )

    def set_start(self, start: float) -> None:
        self.delta.start = start

    def set_end(self, end: float) -> None:
        self.delta.end = end

    def publish(self) -> None:
        self.communicator.publish(
            self.delta, f"{self.module_name}/{self.device_name}/delta/data"
        )

    def set_end_and_publish(self) -> None:
        self.set_end(time())
        self.publish()
