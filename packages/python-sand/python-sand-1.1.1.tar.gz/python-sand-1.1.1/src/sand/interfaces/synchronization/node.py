from __future__ import annotations

from threading import Thread
from typing import Any, Callable

import prctl
from overrides import overrides

from sand.config import CommunicationConfig
from sand.interfaces.communication import Communicator
from sand.logger import Logger


class SandNode(Communicator):
    def __init__(self, communication_config: CommunicationConfig) -> None:
        Communicator.__init__(self, communication_config)

        self.log = Logger(self.__class__.__name__)
        self._threads: list[Thread] = []

    # pylint: disable=too-many-arguments
    def create_thread(
        self,
        target: Callable[..., None],
        args: tuple[Any, ...] = (),
        name: str = "",
        start: bool = False,
        daemon: bool = False,
    ) -> Thread:
        if name == "":
            name = self.__class__.__name__
        self.log.i(f"create Thread: {target.__name__}, {name}", "create_thread")
        thread = Thread(
            target=target,
            args=args,
            name=name,
            daemon=daemon,
        )
        self.add_thread(thread)
        if start:
            thread.start()
        return thread

    @staticmethod
    def set_thread_name(name: str) -> None:
        prctl.set_name(f"SAND_{name}")

    def start_all_threads(self) -> None:
        for thread in self._threads:
            try:
                thread.start()
            except RuntimeError as exception:
                self.log.w(
                    f"Catch runtime exception on startup, still continuing: {exception}",
                    "start_all_threads",
                )

    def get_thread(self, name: str) -> Thread | None:
        for thread in self._threads:
            if thread.name == name:
                return thread
        return None

    def add_thread(self, thread: Thread) -> Thread:
        self._threads.append(thread)
        return thread

    def shutdown_before_join(self) -> None:
        """
        Hook that gets executed before joining the threads and after the events
        have been set
        """

    @overrides
    def shutdown(self) -> None:
        self.log.i(f"Shutdown called for {self.__class__.__name__}", "shutdown")

        # hack, should be done in ShutdownAble who owns this event
        # but then we would need a different mechanism for saying finished, after we actually do so
        self.shutdown_event.set()

        self.shutdown_before_join()

        for thread in self._threads:
            if thread.is_alive():
                self.log.i(f"Shutdown {self.__class__.__name__}", "shutdown")
                thread.join()
            else:
                self.log.i(
                    f"thread {self.__class__.__name__} is None or not alive", "shutdown"
                )

        self.log.i(f"Shutdown finished for {self.__class__.__name__}", "shutdown")

        Communicator.shutdown(self)
