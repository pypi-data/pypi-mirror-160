from __future__ import annotations

from datetime import timedelta

from cv2 import VideoCapture

from sand.config import CameraConfig
from sand.datatypes import ReaderMetric
from sand.interfaces.communication import Communicator
from sand.logger import Logger
from sand.util.time import now


# as it does statistics, it needs that many attributes
# pylint: disable=too-many-instance-attributes
class ReaderStatistics:
    def __init__(self, config: CameraConfig, communicator: Communicator) -> None:
        self.log = Logger(self.__class__.__name__)
        self.next_metric = now()
        self.config = config

        self.communicator = communicator

        self.recorded_frames = 0
        self.dropped_frames = 0
        self.mean_grab_sum = 0.0
        self.mean_grab_counter = 0
        self.mean_retrieve_sum = 0.0
        self.mean_retrieve_counter = 0
        self.start_time = now()
        self.time_for_one_frame: timedelta = timedelta(seconds=-1)

    def _set_next_metric_time(self) -> None:
        self.next_metric = now() + timedelta(seconds=self.config.metric_interval)

    def log_metric(self, force: bool = False) -> None:
        if now() > self.next_metric or force:
            self._set_next_metric_time()
            end_time = now()
            time_delta = end_time - self.start_time
            frames_per_second = (
                self.recorded_frames / time_delta.total_seconds()
                if time_delta.total_seconds() != 0
                else float("inf")
            )
            time_for_one_frame = (
                (1 / frames_per_second) if frames_per_second != 0 else float("inf")
            )

            reader_metric = ReaderMetric(self.config.name)
            if self.mean_grab_counter == 0:
                self.mean_grab_counter = 1  # fix division by zero in --check
            if self.mean_retrieve_counter == 0:
                self.mean_retrieve_counter = 1  # fix division by zero in --check
            reader_metric.set_int_field("recorded_frames", self.recorded_frames)
            reader_metric.set_int_field("dropped_frames", self.dropped_frames)
            reader_metric.set_float_field("mean_grab_sum", round(self.mean_grab_sum, 6))

            reader_metric.set_int_field("mean_grab_counter", self.mean_grab_counter)
            reader_metric.set_float_field(
                "mean_grab_time", round(self.mean_grab_sum / self.mean_grab_counter, 6)
            )
            reader_metric.set_float_field(
                "mean_retrieve_sum", round(self.mean_retrieve_sum, 6)
            )
            reader_metric.set_int_field(
                "mean_retrieve_counter", self.mean_retrieve_counter
            )
            reader_metric.set_float_field(
                "mean_retrieve_time",
                round(self.mean_retrieve_sum / self.mean_retrieve_counter, 6),
            )

            reader_metric.set_float_field("time_for_one_frame", time_for_one_frame)
            reader_metric.set_float_field("config_fps", float(self.config.fps))
            reader_metric.set_float_field("camera_fps", frames_per_second)
            self.communicator.publish(
                reader_metric.get_point(),
                f"{self.communicator.__class__.__name__}/{self.config.name}/data/metric",
            )

    def log_statistics(
        self, successful_grab: bool, successful_retrieve: bool, stream: VideoCapture
    ) -> None:
        end_time = now()
        time_delta = end_time - self.start_time
        excepted_frames = int(time_delta.total_seconds() * self.config.fps)
        frames_per_second = (
            int(self.recorded_frames / time_delta.total_seconds())
            if time_delta.total_seconds() != 0
            else float("inf")
        )
        self.log.d(
            (
                f"start_time: {self.start_time.strftime('%H:%M:%S.%f')} | "
                f"end_time: {end_time.strftime('%H:%M:%S.%f')} | "
                f"time_delta: {time_delta} | frames: {self.recorded_frames} | "
                f"exp_frames: {excepted_frames} | FPS: {frames_per_second} | "
                f"successful_grab: {successful_grab} | successful_retrieve: {successful_retrieve} | "
                f"stream.isOpened: {stream.isOpened()} | stream.getExceptionMode: {stream.getExceptionMode()}"
            ),
            "log_statistics",
        )

    def add_dropped_frame(self) -> None:
        self.dropped_frames += 1

    def add_grab_time(self, time: timedelta) -> None:
        self.mean_grab_sum += time.total_seconds()
        self.mean_grab_counter += 1

    def add_retrieve_time(self, time: timedelta) -> None:
        self.mean_retrieve_sum += time.total_seconds()
        self.mean_retrieve_counter += 1

    def add_frame(self) -> None:
        self.recorded_frames += 1
