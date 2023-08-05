from __future__ import annotations

from copy import copy
from time import time

from sand.config import SandConfig
from sand.datatypes import Datapoint, Topic
from sand.datatypes.delta import Delta
from sand.interfaces.synchronization import SandNode

# we have a problem...
# we "lose" some frames through the process of generating our map and the neural network
# for example: 25fps from camera, the neural network only can process 15 fps and the map builder builds the map with 5fps
# if we build the stats with the output of the map builder, we lose many stat informationen.
from sand.util.per_second import PerSecondHelper

# solution for frames:
# we collect all frames and extract the stats after a livetime > max process time.
# -> we get all informations, also from "dropped frames".
# or
# we collect all frames and set an "processed" flag
# -> problem with dropped frames
#
# solution for maps:
# we collect the maps and generate a seperate stat


class Calculator:
    def __init__(self, device_name: str, data_id: int):
        self.creation_time = time()
        self.device_name = device_name
        self.data_id = data_id
        self.deltas: list[tuple[str, Delta]] = []

    def add(self, delta: Delta, source: str) -> None:
        self.deltas.append((source, delta))

    def find_source(self, source: str) -> Delta | None:
        for datasource, delta in list(self.deltas):
            if datasource == source:
                return delta
        return None

    def calc(self) -> list[str]:
        metrics: list[str] = []
        for datasource, delta in list(self.deltas):

            point = Datapoint()
            point.point["measurement"] = "delta"
            point.set_tag("device", self.device_name)
            point.set_tag("module", datasource)
            point.set_float_field("delta_processing", float(delta.end - delta.start))
            metrics.append(point.get_point())

            for source_name in delta.source.split(","):
                source = self.find_source(source_name)
                if source is not None:
                    point = Datapoint()
                    point.point["measurement"] = "delta_to"
                    point.set_tag("device", self.device_name)
                    point.set_tag("receiver", source_name)
                    point.set_tag("sender", datasource)
                    point.set_float_field("delta", float(delta.start - source.end))
                    metrics.append(point.get_point())

        return metrics

    def check(self) -> bool:
        return self.creation_time + 2 <= time()


class DeltaCollector(SandNode):
    def __init__(self, global_config: SandConfig) -> None:
        SandNode.__init__(self, global_config.communication)

        self.stats_per_second = PerSecondHelper(
            self,
            "stats_per_second",
            "all",
        )

        self.store: dict[str, Calculator] = {}

        self.subscribe_topic("+/+/delta/data", self.push_timestamp)

        self.create_thread(
            target=self.work, args=(), name=DeltaCollector.__name__, start=True
        )
        self.set_thread_name("dc_Main")

    def push_timestamp(self, topic: Topic, calc_delta: Delta) -> None:
        name = calc_delta.device_name
        frame_id = calc_delta.id
        ident = f"{name}_{frame_id}"
        if ident not in self.store:
            self.store[ident] = Calculator(name, frame_id)
        self.store[ident].add(calc_delta, topic.split("/")[0])

    def work(self) -> None:
        self.set_thread_name("dc_work")
        while not self.shutdown_event.is_set():
            store_copy = copy(self.store)
            for ident in store_copy:
                if store_copy[ident].check():
                    data = self.store.pop(ident)
                    metric = data.calc()
                    self.publish(
                        metric,
                        f"{DeltaCollector.__name__}/{data.device_name}/metric/data",
                    )
            self.stats_per_second.inc_and_publish()
            self.shutdown_event.wait(0.01)
