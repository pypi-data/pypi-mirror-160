from __future__ import annotations

from datetime import timedelta
from socket import timeout

from sand.config import LidarConfig, SandConfig
from sand.datatypes import LidarPacket
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import LidarSubscriber
from sand.reader.lidar.reader import LidarFileReader, Vlp16Reader
from sand.util.per_second import PerSecondHelper
from sand.util.time_management import TimeManagement


class LidarReader(SandNode):
    def __init__(
        self, config: LidarConfig, playback: bool, sand_config: SandConfig
    ) -> None:
        SandNode.__init__(self, communication_config=sand_config.communication)
        self.config = config
        self.subscribers: list[LidarSubscriber] = []
        self.playback = playback
        self.playback_timediff = timedelta(0)
        self.time_management = TimeManagement(
            fps=150 if self.playback else 200,
            slowdown_factor=1,
            shutdown_event=self.shutdown_event,
        )
        self.pps = PerSecondHelper(self, "pps", f"lidar_reader/{self.config.name}", 150)
        if self.config.active:
            if self.playback and self.config.file_path != "":
                self.device: LidarFileReader | Vlp16Reader = LidarFileReader(
                    self.config, self.log
                )
            else:
                if self.playback:
                    self.log.d(
                        "playback but there is no lidar file - open sockets", "init"
                    )
                self.device = Vlp16Reader(self.config, self.log)

            self.create_thread(
                target=self.read, args=(), name=f"lr_{self.config.name}", start=True
            )

            self.log.i(
                f"{self.config.name} started with port {self.config.data_port}",
                "Vlp16Reader",
            )

    def subscribe(self, subscriber: LidarSubscriber) -> None:
        self.subscribers.append(subscriber)

    def get_packet(self) -> bytes:
        return self.device.get_packet()

    def read(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}_read")
        timeouts = 0
        while not self.shutdown_event.is_set():
            try:
                if not self.time_management.wait_for_next_frame():
                    self.log.d("shutdown occurred", "read")
                    break

                data = self.get_packet()
                if len(data) > 0:
                    timeouts = 0
                    packet = LidarPacket(self.config.name, data)
                    for subscriber in self.subscribers:
                        subscriber.push_packet(packet)
                self.pps.inc_and_publish()
            except timeout:
                if not timeouts % 100:
                    self.log.w(f"{self.config.name} timeout", "read")
                timeouts += 1
            except AssertionError:
                self.log.exception("Assertion Error while capturing lidar", "read")
            except Exception:  # pylint: disable=broad-except
                self.log.exception("General Exception while capturing lidar", "read")

        if self.playback and self.config.file_path != "":
            self.device.close()
