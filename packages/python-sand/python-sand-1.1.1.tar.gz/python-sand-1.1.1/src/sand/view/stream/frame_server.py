from __future__ import annotations

from http.server import HTTPServer
from socketserver import ThreadingMixIn
from threading import Event

from sand.config import SandConfig
from sand.datatypes import Image, SandBoxes


class FrameServer(ThreadingMixIn, HTTPServer):
    frame: Image
    shutdown_event: Event
    config: SandConfig
    num_classes: int = 1000
    boxes: SandBoxes | None = None
