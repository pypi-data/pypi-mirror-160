from __future__ import annotations

from time import time

from sand.datatypes import Datapoint
from sand.interfaces.communication import Communicator

# pylint: disable=too-many-instance-attributes, too-many-arguments


class PerSecondHelper:
    def __init__(
        self,
        communicator: Communicator,
        name: str,
        device: str,
        expected: int = 0,
        tags: dict[str, str | int] | None = None,
    ) -> None:
        self.expected = expected
        self.start_time = time()
        self.sum_total = 0.0
        self.last_time = time()
        self.last_time_publish = time()
        self.publish_every_seconds = 10.0
        self.last_segment = 0.0
        self.sum_last_segment = 0.0
        self.communicator = communicator
        self.name = name
        self.base_topic = f"{communicator.__class__.__name__}/{device}"
        self.tags: dict[str, str | int] = {} if tags is None else tags
        self.min: float | None = None
        self.max: float | None = None

    def calc(self) -> None:
        timestamp = time()
        diff_seconds = int(timestamp) - int(self.last_time)
        if diff_seconds > 0:
            self.last_segment = self.sum_last_segment / diff_seconds
            self.sum_last_segment = 0
            self.min = None
            self.max = None

        self.last_time = timestamp

    def inc(self) -> None:
        self.calc()
        self.sum_total += 1
        self.sum_last_segment += 1

    def add(self, data: float) -> None:
        self.calc()
        self.sum_total += data

        self.sum_last_segment += data
        if self.max is None or data > self.max:
            self.max = data
        if self.min is None or data < self.min:
            self.min = data

    def reset_time(self) -> None:
        self.sum_total = 0
        self.sum_last_segment = 0
        self.start_time = time()

    def get_sum_total(self) -> float:
        return self.sum_total

    def get_per_second_average(self) -> float:
        return self.sum_total / (time() - self.start_time)

    def get_per_second(self) -> float:
        return self.last_segment

    def get_error_average(self) -> float:
        return self.expected - self.get_per_second_average()

    def get_error(self) -> float:
        return self.expected - self.last_time

    def inc_and_publish(self) -> None:
        self.inc()
        self.publish()

    def add_and_publish(self, data: float) -> None:
        self.add(data)
        self.publish()

    def publish(self) -> None:
        if self.last_time_publish + self.publish_every_seconds <= time():
            base_topic_split = self.base_topic.split("/")
            source_modul = base_topic_split[0]
            device = base_topic_split[1]
            datapoint = Datapoint()
            datapoint.point["measurement"] = "per_second"
            datapoint.set_tags(self.tags)
            datapoint.set_tag("module", source_modul)
            datapoint.set_tag("device", device)
            datapoint.set_tag("type", self.name)
            datapoint.set_float_field("ops", self.get_per_second())
            datapoint.set_float_field("ops_average", self.get_per_second_average())
            if self.min is not None:
                datapoint.set_float_field("ops_min", self.min)
            if self.max is not None:
                datapoint.set_float_field("ops_max", self.max)
            if self.expected != 0:
                datapoint.set_float_field("ops_error", self.get_error())
                datapoint.set_float_field("ops_average_error", self.get_error_average())
            self.last_time_publish = time()
            self.communicator.publish(
                datapoint.get_point(), f"{self.base_topic}/metric/data"
            )

    def __str__(self) -> str:
        return f"average: {self.get_per_second_average()}, actual: {self.last_segment}, expected: {self.expected}"
