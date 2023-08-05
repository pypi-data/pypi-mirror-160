from __future__ import annotations

import os
from functools import partial
from pathlib import Path

from overrides import EnforceOverrides

from sand.cli.arguments import Arguments
from sand.config import CommunicationConfig

# pylint: disable=import-outside-toplevel


class SandStarter(EnforceOverrides):
    """This is the starter of the whole system."""

    def setup_isolated_gpu_system(
        self,
        config: Path,
        playback_path: Path | None,
        gpu_index: int,
        gpu_count: int,
    ) -> None:
        """This function is in the {Isolator} setup with envionment-isolated GPUs.

        It starts the real system and is the first one that actually imports
        the rest of the system. Up until this point everything imports just
        very small bits of the system.

        You can choose to override this function if you want to keep the CLI,
        the {Isolator}-setup and the GPU isolation as well, but want to define
        your own system entirely.
        """

        # gets loaded in isolated environment; therefore nothing shared
        from sand.definition import define_system

        define_system(
            config,
            playback_path,
            gpu_index,
            gpu_count,
        )

    def setup_isolated_system(
        self,
        config: Path,
        playback_path: Path | None,
        gpu_index: int,
        gpu_count: int,
    ) -> None:
        """This function gets executed in its on {Isolator} and then sets GPU environment variables.

        You can choose to override this function if you want to keep the CLI
        like it is by default and also want the {Isolator}-setup.
        """
        if gpu_count > 0:
            os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_index}"

        self.setup_isolated_gpu_system(
            config,
            playback_path,
            gpu_index,
            gpu_count,
        )

    def start_system(self, arguments: Arguments) -> None:
        """This is the original main function of SAND.

        It starts a Main-instance and also a, depending on {arguments.gpu},
        number of {Isolator}s that normally execute {self.setup_system}.

        You can choose to override this function, if you want to completely
        your own starting process but keep the CLI like it is.
        """
        # pylint: disable=import-outside-toplevel
        from sand.interfaces.synchronization import Isolator
        from sand.main import Main

        # start main initially as it manages the shutdown for both sub-systems
        main = Main(
            arguments.logger_listener,
            ignore_on_shutdown=arguments.ignore_on_shutdown,
        )

        for gpu in range(max(arguments.gpus, 1)):
            # must not be daemons as it will have sub-processes again and
            # daemons are not allowed additional sub-processes
            Isolator(
                target=partial(
                    self.setup_isolated_system,
                    config=arguments.config,
                    playback_path=arguments.playback,
                    gpu_index=gpu,
                    gpu_count=arguments.gpus,
                ),
                communication_config=CommunicationConfig(),
                daemon=False,
            )

        main.spin(arguments.check)
