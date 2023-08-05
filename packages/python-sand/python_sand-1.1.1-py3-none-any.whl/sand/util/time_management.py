from __future__ import annotations

from threading import Event
from time import time


class TimeManagement:
    def __init__(
        self,
        fps: int,
        slowdown_factor: int,
        sleep_time_fraction: int = 2,
        shutdown_event: Event = Event(),
    ) -> None:
        self.shutdown_event = shutdown_event
        self.time_between_frames = 1 / (fps / slowdown_factor)
        self.start_time = time()
        self.frame_count = 0
        self.next_frame_time = self.start_time

        self.sleep_time = self.time_between_frames / sleep_time_fraction

    def is_time_for_next_frame(self) -> bool:
        return time() >= self.next_frame_time

    def increase_frame_count(self) -> None:
        self.frame_count += 1
        self.next_frame_time = (
            self.start_time + self.frame_count * self.time_between_frames
        )

    def get_sleep_time(self) -> float:
        return self.sleep_time

    def reset_time(self) -> None:
        self.frame_count = 0
        self.start_time = time()
        self.next_frame_time = self.start_time

    def wait_for_next_frame(self) -> bool:
        """Convenience method to wait until it's time for the next frame.

        It has limited precision that is mainly influenced by
        {sleep_time_fraction}, therefore if you need higher precision you should
        do it yourself.

        :returns
            True if it is time for the next frame

            False if a shutdown occurred
        """
        while not self.shutdown_event.is_set():
            if self.is_time_for_next_frame():
                self.increase_frame_count()
                return True

            self.shutdown_event.wait(self.get_sleep_time())
        return False
