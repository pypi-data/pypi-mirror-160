from __future__ import annotations

import json
from _thread import start_new_thread
from datetime import timedelta
from pathlib import Path
from subprocess import CalledProcessError, check_output

from sand.config import CameraConfig
from sand.datatypes import RecorderMetric, RecorderSegmentMetric
from sand.interfaces.communication import Communicator
from sand.logger import Logger
from sand.util.time import now


class VideoWriterThreadStatistics:
    def __init__(
        self,
        config: CameraConfig,
        write_folder: Path,
        communicator: Communicator,
    ):
        self.log = Logger(self.__class__.__name__)
        self.communicator = communicator
        self.stream_name: str = config.name
        self.fps: float = config.fps

        self.start_segment = now()
        self.end_segment = now()
        self.file_name = (
            f"{self.start_segment.strftime('%Y-%m-%dT%H:%M:%S')}_{config.name}.mp4"
        )
        self.path_to_segment_file = write_folder.joinpath(self.file_name)

        self.frame_count = 0
        self.queue_count = 0

    def _get_file_information(
        self,
    ) -> tuple[dict[str, str] | None, dict[str, str] | None, dict[str, str] | None]:
        file_infos = None
        if not self.path_to_segment_file.exists():
            return None, None, None
        try:
            file_infos = json.loads(
                check_output(
                    f"ffprobe -loglevel quiet -print_format json -show_format -show_streams "
                    f"file:{self.path_to_segment_file.as_posix()}",
                    shell=True,
                )
            )
        except CalledProcessError:
            self.log.exception(
                "Could not access information about segment", "intermediary"
            )
        stream = None
        if (
            file_infos is not None
            and "streams" in file_infos
            and len(file_infos["streams"]) > 0
        ):
            stream = file_infos["streams"][0]
        fmt = file_infos["format"] if file_infos is not None else None
        return stream, fmt, file_infos

    def _log_segment_metrics(self, fmt: dict[str, str] | None) -> None:
        # build metrics to export in influxdb
        recorder_metric = RecorderSegmentMetric(self.stream_name)
        recorder_metric.set_int_field("segment_frames", self.frame_count)
        segment_fps = (
            self.frame_count / (self.end_segment - self.start_segment).total_seconds()
        )
        recorder_metric.set_float_field("segment_fps", segment_fps)
        recorder_metric.set_float_field(
            "segment_mean_queue_count", self.get_mean_queue_count()
        )
        if fmt is not None:
            recorder_metric.set_float_field(
                "file_bitrate", float(fmt.get("bit_rate", 0.0))
            )
            recorder_metric.set_int_field("file_size", int(fmt["size"]))

        self.communicator.publish(
            recorder_metric.get_point(),
            f"{self.communicator.__class__.__name__}/{self.stream_name}/metric/data",
        )

    def _build_stats_string(
        self,
        stream: dict[str, str] | None,
        fmt: dict[str, str] | None,
        file_infos: dict[str, str] | None,
    ) -> str:
        # build log string for output in console and logfile
        stats_string = "\n\n"
        stats_string += f"""Statistics for stream: {self.stream_name}
            target fps: {self.fps}"""
        stats_string += "\n\n"
        stats_string += f"""Segment (calculated): {self.file_name}
            segment_processing_start: {self.start_segment}
            segment_processing_end: {self.end_segment}
            segment_processing_duration: {(self.end_segment - self.start_segment)}
            segment_frames: {self.frame_count}
            segment_fps: {self.frame_count / (self.end_segment - self.start_segment).total_seconds()}
            mean_queue_count: {self.get_mean_queue_count()}"""

        stats_string += "\n\n"
        stats_string += (
            f"""Segment (actual): {self.file_name}
            codec: {stream['codec_long_name']}
            resolution: {stream['width']} x {stream['height']}
            avg framerate: {stream['avg_frame_rate']}
            stream duration (sec): {stream['duration']}
            format duration (sec): {fmt['duration']}
            bit_rate: {fmt['bit_rate']}
            file size: {int(fmt['size']) / 1024 / 1024} MB"""
            if file_infos is not None and stream is not None and fmt is not None
            else "No actual file_infos available"
        )
        return stats_string

    def get_mean_queue_count(self) -> float:
        return float(
            self.queue_count / self.frame_count if self.frame_count != 0 else 1
        )

    def log_metric(self) -> None:
        _stream, fmt, _file_infos = self._get_file_information()
        self._log_segment_metrics(fmt)

    def log_statistics(self) -> None:
        stream, fmt, file_infos = self._get_file_information()
        stats_string = self._build_stats_string(stream, fmt, file_infos)
        self.log.d(stats_string, "log_segment_statistics")
        start_new_thread(
            self._write_logfile,
            (
                self.path_to_segment_file.with_suffix(".log"),
                stats_string,
            ),
        )

    def _write_logfile(self, logfile: Path, message: str) -> None:
        try:
            logfile.write_text(message)
        except FileNotFoundError:
            self.log.exception(
                f"FileNotFoundError when writing stats to: {logfile}", "_write_logfile"
            )


class VideoRecorderStatistics:
    def __init__(self, config: CameraConfig, communicator: Communicator) -> None:
        self.stream_name: str = config.name
        self.fps: float = config.fps
        self.config = config

        self.log = Logger(self.__class__.__name__)
        self.communicator = communicator

        # threads stats
        self.threads: list[VideoWriterThreadStatistics] = []
        self.next_metric = now()

    def _set_next_metric_time(self) -> None:
        self.next_metric = now() + timedelta(seconds=self.config.metric_interval)

    def new_writer_stats(self, write_folder: Path) -> VideoWriterThreadStatistics:
        stats = VideoWriterThreadStatistics(
            self.config, write_folder, self.communicator
        )
        self.threads.append(stats)
        return stats

    def remove_writer_stats(self, obj: VideoWriterThreadStatistics) -> None:
        self.threads.remove(obj)

    def log_metric(self) -> None:
        if now() > self.next_metric and len(self.threads) > 0:
            self._set_next_metric_time()
            recorder_metric = RecorderMetric(self.stream_name)
            recorder_metric.set_int_field("active_threads", len(self.threads))
            current_thread = self.threads[len(self.threads) - 1]
            recorder_metric.set_int_field("queue_count", current_thread.queue_count)
            recorder_metric.set_int_field("frame_count", current_thread.frame_count)
            recorder_metric.set_float_field(
                "mean_queue_size",
                current_thread.queue_count
                / (
                    current_thread.frame_count if current_thread.frame_count != 0 else 1
                ),
            )

            total_queue_size = 0
            total_frame_count = 0
            for thread in self.threads:
                total_queue_size += thread.queue_count
                total_frame_count += thread.frame_count

            recorder_metric.set_int_field("total_queue_size", total_queue_size)
            recorder_metric.set_int_field("total_frame_size", total_frame_count)
            recorder_metric.set_float_field(
                "mean_total_queue_size",
                total_queue_size / (total_frame_count if total_frame_count != 0 else 1),
            )
            self.communicator.publish(
                recorder_metric.get_point(),
                f"{self.communicator.__class__.__name__}/{self.stream_name}/metric/data",
            )
