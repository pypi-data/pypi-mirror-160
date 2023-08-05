from __future__ import annotations

from datetime import timedelta
from glob import glob
from pathlib import Path
from re import match
from subprocess import PIPE, Popen

from sand.config import ConverterConfig
from sand.logger import Logger
from sand.util.camera import is_sand_visual_camera


def _filter_h264(files: list[Path]) -> list[Path]:
    return list(filter(lambda file: match(r".*h264.*", file.name) is None, files))


class Convert:
    __DEFAULT_PATH = Path("/tmp")

    def __init__(self, config: ConverterConfig, log: Logger) -> None:
        self.config = config
        self.log = log
        self.folders: list[Path] = list(map(Path, self.config.folders))
        self.current_working_folder = self.__DEFAULT_PATH

        self.duration_visual = timedelta(
            seconds=self.config.segment_length_sec / self.config.speedup_visual
        )
        self.duration_thermal = timedelta(
            seconds=self.config.segment_length_sec / self.config.speedup_thermal
        )

    def get_file_list(self) -> list[Path]:
        fct = "get_file_list"

        file_list: list[Path] = []
        for folder in self.folders:
            file_list.extend(
                list(map(Path, glob(f"{folder.as_posix()}/**/*.mp4", recursive=True)))
            )

        non_encoded_list = _filter_h264(file_list)
        self.log.d(f"Without h264: {non_encoded_list}", fct)

        list_without_working = self._filter_current_working_folder(non_encoded_list)
        self.log.i(
            f"Ignored current folder: {self.current_working_folder.as_posix()} | "
            f"Converting files: {list_without_working}",
            fct,
        )

        return list_without_working

    def get_timeout_for_file(self, file: Path) -> timedelta:
        if is_sand_visual_camera(file.name):
            return self.duration_visual
        return self.duration_thermal

    def _filter_current_working_folder(self, files: list[Path]) -> list[Path]:
        return list(
            filter(
                lambda file: not file.as_posix().startswith(
                    self.current_working_folder.as_posix()
                ),
                files,
            )
        )

    def set_current_working_folder(self, path: Path) -> bool:
        initial_change = self.current_working_folder == self.__DEFAULT_PATH
        self.current_working_folder = path
        return initial_change

    def convert_process(self, source_file: Path, target_file: Path) -> Popen[bytes]:
        return Popen(
            f"ffmpeg -i file:{source_file} -loglevel repeat+level+debug -hide_banner -y -c:v h264_nvenc -rc:v vbr_hq "
            f"-cq:v 19 -b:v 2500k -maxrate:v 5000k -profile:v high -preset fast -gpu {self.config.gpu_index} "
            f"file:{target_file} 2>&1",
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
        )

    def start_and_wait(self, source_file: Path, target_file: Path) -> tuple[str, str]:
        with self.convert_process(source_file, target_file) as process:
            stdout, stderr = process.communicate()
            return stdout.decode(), stderr.decode()
