from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from subprocess import Popen

from overrides import overrides

from sand.config import ConverterConfig, SandConfig
from sand.converter.convert import Convert
from sand.datatypes import ConverterMetric, Topic
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.synchronization import SandNode
from sand.util.camera import get_camera_name
from sand.util.time import now


def get_converted_file_name(file: Path) -> Path:
    return file.with_suffix(f".h264{file.suffix}")


class Converter(SandNode, ConfigurationManager[ConverterConfig]):
    __DEFAULT_PATH = Path("/tmp")

    def __init__(
        self,
        global_config: SandConfig,
    ) -> None:
        SandNode.__init__(self, communication_config=global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)
        self.convert = Convert(self.config, self.log)
        self.current_working_folder = Path("")
        self.create_thread(target=self.work)
        self.subscribe_topic("DriveWatcher/all/data/segment", self.path_change)

    @overrides
    def select_config(self, global_config: SandConfig) -> ConverterConfig:
        return global_config.converter

    def path_change(self, _: Topic, absolute_path: str) -> None:
        initial_change = self.convert.set_current_working_folder(self.__DEFAULT_PATH)
        self.current_working_folder = Path(absolute_path)

        if initial_change:
            self.log.i("Starting converter daemon", "path_change")
            self.start_all_threads()

    def work(self) -> None:
        self.set_thread_name(f"{self.__class__.__name__}_{self.log.name}")

        self.log.i(
            f"Offsetting first scan by {self.config.scan_start_offset_sec} seconds",
            "work",
        )
        self.shutdown_event.wait(self.config.scan_start_offset_sec)

        while not self.shutdown_event.is_set():
            self._convert()

            self.log.i(
                f"Waiting for next scan: {self.config.scan_interval_sec} sec", "work"
            )
            self.shutdown_event.wait(self.config.scan_interval_sec)

        self.log.i("Converter-Daemon shutting down", "work")

    def _create_metric(
        self, file: Path, shutdown_break: bool, timeout: bool, duration: timedelta
    ) -> None:
        metric = ConverterMetric(get_camera_name(file=file.name, default=file.name))

        metric.set_int_field("shutdown", 1 if shutdown_break else 0)
        metric.set_int_field("timeout", 1 if timeout else 0)
        metric.set_float_field("duration_sec", duration.total_seconds())
        self.publish(metric.get_point(), "converter/all/metric/data")

    def _convert(self) -> None:
        fct = "convert"

        list_without_working = self.convert.get_file_list()
        for source_file in list_without_working:
            target_file = get_converted_file_name(source_file)
            file_timeout = self.convert.get_timeout_for_file(source_file)

            # self.log.i(f"Converting file: {file} | timeout: {file_timeout}", fct)

            with self.convert.convert_process(
                source_file, target_file
            ) as convert_process:

                # self.log.d(f"[{file}] started converter", fct)

                timeout, duration = self._poll_process(
                    convert_process, source_file, target_file, file_timeout
                )

                self._create_metric(
                    source_file, self.shutdown_event.is_set(), timeout, duration
                )

                if self.shutdown_event.is_set():
                    self.log.w(
                        f"[{source_file}] Shutdown while converting, deleting interrupted conversion result",
                        fct,
                    )
                    convert_process.terminate()
                    target_file.unlink()
                    return

                stdout, stderr = convert_process.communicate()
                self.log.d(
                    f"[{source_file}] Convert log: {stdout.decode('utf-8')}\nstderr: {stderr.decode('utf-8')}",
                    fct,
                )

                if timeout:
                    self.log.w(
                        f"[{source_file}] Conversion timeout, removing old file", fct
                    )
                    target_file.unlink()
                    continue

                if self.config.delete_after_conversion:
                    self.log.i(f"[{source_file}] Success! Removing old file", fct)
                    source_file.unlink()

    def _poll_process(
        self,
        process: Popen[bytes],
        file: Path,
        converted: Path,
        timeout: timedelta,
    ) -> tuple[bool, timedelta]:
        fct = "_poll_process"
        is_timeout = False
        start = now()
        while not self.shutdown_event.is_set():
            if process.poll() is not None:
                self.log.i(f"[{file}] Successfully converted to {converted}", fct)
                break

            duration = now() - start
            if duration > timeout:
                self.log.w(
                    f"[{file}] Converting takes longer than timeout, aborting...",
                    fct,
                )
                process.terminate()
                is_timeout = True
                break

            self.log.d(
                f"[{file}] Waiting {self.config.process_poll_interval_sec} sec for next poll",
                fct,
            )
            self.shutdown_event.wait(self.config.process_poll_interval_sec)

        return is_timeout, now() - start
