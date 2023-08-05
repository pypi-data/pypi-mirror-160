from __future__ import annotations

import json
from threading import Lock
from typing import Any

from influxdb_client import InfluxDBClient
from overrides import overrides

from sand.config import MetricConfig, SandConfig
from sand.datatypes import Topic
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.util.per_second import PerSecondHelper


class Committer(SandNode, ConfigurationManager[MetricConfig]):
    def __init__(self, global_config: SandConfig) -> None:
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        self.items: list[dict[str, Any]] = []
        self.__item_lock = Lock()
        self.metric_per_seconds = PerSecondHelper(self, "metric_per_seconds", "all")

        if self.config.active and self._should_commit_in_db():
            self.influx = InfluxDBClient(
                url=self.config.influx_url,
                token=self.config.influx_token,
                org=self.config.influx_org,
            )
            self.influx_write_api = self.influx.write_api()
            self.subscribe_topic("+/+/metric/data", self.commit)

            self.create_thread(
                target=self.work,
                args=(),
                name="committer",
                start=True,
            )

    @overrides
    def select_config(self, global_config: SandConfig) -> MetricConfig:
        return global_config.metric

    def _should_commit_in_db(self) -> bool:
        return self.config.commit_in_db

    # thread function
    # commits metrics when size(queue) > batch_size
    def commit(self, _: Topic, payload: list[str] | str) -> None:
        assert (
            self.config.active and self._should_commit_in_db()
        ), "Object needs to be able to write to the API, otherwise this method causes a memory leak"

        # lock to make sure we don't miss updates while resetting
        with self.__item_lock:
            if isinstance(payload, str):
                self.items.append(json.loads(payload))
            else:
                self.items += list(map(json.loads, payload))

            if len(self.items) > self.config.batch_size:
                self.influx_write_api.write(
                    bucket="sand",
                    org=self.config.influx_org,
                    record=self.items,
                )
                self.items = []
                self.metric_per_seconds.inc_and_publish()

    def work(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}")
        # keep the process alive, but do nothing
        self.shutdown_event.wait()
