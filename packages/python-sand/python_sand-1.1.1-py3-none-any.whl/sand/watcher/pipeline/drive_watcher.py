from __future__ import annotations

from pathlib import Path
from shutil import disk_usage

import prctl
from overrides import overrides

from sand.config import DriveWatcherConfig, SandConfig
from sand.interfaces.config import ConfigurationManager
from sand.interfaces.shutdown import ShutdownAble
from sand.interfaces.synchronization import SandNode
from sand.util.time import now


class DriveWatcher(SandNode, ConfigurationManager[DriveWatcherConfig]):
    def __init__(self, global_config: SandConfig) -> None:
        SandNode.__init__(self, global_config.communication)
        ConfigurationManager.__init__(self, self, global_config)

        # own folder array needed for reordering
        self.folders = list(map(Path, self.config.folders))
        self.memory_remaining = self.config.memory_remaining_gb * 1024 * 1024 * 1024

        self._current_folder = Path("/tmp")
        self.create_thread(
            target=self.watch, args=(), name=self.__class__.__name__, start=True
        )

    @overrides
    def select_config(self, global_config: SandConfig) -> DriveWatcherConfig:
        return global_config.watcher

    @property
    def current_folder(self) -> Path:
        return self._current_folder

    @current_folder.setter
    def current_folder(self, value: Path) -> None:
        self._current_folder = value

        self.publish(
            topic=f"{DriveWatcher.__name__}/all/data/segment",
            payload=self._current_folder.absolute().as_posix(),
            retain=True,
            qos=1,
        )
        self.publish(
            topic=f"{DriveWatcher.__name__}/all/data/moment",
            payload=self._get_moment_folder(self.current_folder).absolute().as_posix(),
            retain=True,
        )

    @staticmethod
    def _get_moment_folder(folder: Path) -> Path:
        return folder.parent.parent.joinpath("moments")

    def get_folder(self) -> Path | None:
        fct = "get_folder"
        found_folder = None
        for folder in self.folders:
            _total, _used, free = disk_usage(folder.as_posix())

            if free > self.memory_remaining:
                self.log.i(
                    f"{folder} has memory left | free: {free} B | target: {self.memory_remaining} B",
                    fct,
                )
                found_folder = folder
                break

            self.log.w(
                f"{folder} has no memory left | free: {free} B | target: {self.memory_remaining} B",
                fct,
            )

        if found_folder is not None and self.folders[0] != found_folder:
            # put found folder at the front, then in next iteration is found first
            # therefore we can achieve longer connected segments in one folder, instead of flipping when converting
            self.folders.remove(found_folder)
            self.folders.insert(0, found_folder)

        return found_folder

    def wait_for_next_change(self) -> None:
        self.log.i(
            f"Going to sleep for: {self.config.segment_length_secs} s",
            "wait_for_next_change",
        )
        self.shutdown_event.wait(self.config.segment_length_secs)

    @staticmethod
    def _get_folder_prefix(folder: Path) -> Path:
        return folder.joinpath("recordings", "uncategorized")

    def watch(self) -> None:
        prctl.set_proctitle(f"{self.__class__.__name__}_{self.log.name}")
        fct = "watch"
        while not self.shutdown_event.is_set():
            folder = self.get_folder()

            if folder is None:
                self.log.c("We have no folder left to write in!", fct)

                self._shutdown_system()

                return

            new_folder = self._get_folder_prefix(folder).joinpath(
                now().strftime("%Y-%m-%dT%H:%M:%S"),
            )
            try:
                # also creates intermediate directories to contain the "leaf"
                new_folder.mkdir(parents=True, exist_ok=True)
                self._get_moment_folder(new_folder).mkdir(parents=True, exist_ok=True)
            except PermissionError:
                self.log.exception(
                    f"No permission to create sub folders in {folder}, killing System...",
                    fct,
                )
                self._shutdown_system()
                return

            self.log.i(f"Changing folder to: {new_folder}", fct)
            self.current_folder = new_folder

            self.wait_for_next_change()

    def _shutdown_system(self) -> None:
        self.publish(
            payload=f"{now()}",
            topic=ShutdownAble.get_shutdown_topic(),
            retain=True,
        )
