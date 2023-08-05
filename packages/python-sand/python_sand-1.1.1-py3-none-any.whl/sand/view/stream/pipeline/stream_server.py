from __future__ import annotations

from numpy import uint8, zeros
from overrides import overrides

from sand.config import CommunicationConfig
from sand.datatypes import Dimensions, EnrichedFrame, SandBoxes, Topic
from sand.interfaces.synchronization import SandNode
from sand.interfaces.util import CollectAble, EnrichedSubscriber
from sand.util.time_management import TimeManagement
from sand.view.stream.frame_server import FrameServer
from sand.view.stream.mjpeg_handler import MjpegHandler


class StreamServer(SandNode, EnrichedSubscriber):
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        name: str,
        port: int,
        resolution: Dimensions,
        communication_config: CommunicationConfig,
        source: CollectAble[EnrichedSubscriber],
    ):
        SandNode.__init__(self, communication_config)
        self.time_management = TimeManagement(1, slowdown_factor=1)
        self.source = "CameraReader"
        self.name = name
        source.subscribe(self)
        server_adress = "0.0.0.0"
        self.log.d(
            f"start MJPEG Server on {server_adress}:{port}",
            "StreamServer",
        )
        self.server = FrameServer((server_adress, port), MjpegHandler)
        self.subscribe_topic(f"NeuralNetwork/{name}/data/boxes", self.push_neural_frame)
        self.subscribe_topic("NeuralNetwork/all/data/num_classes", self.set_num_classes)

        # noinspection PyTypeChecker
        self.server.frame = zeros(
            (
                resolution.width,
                resolution.height,
                3,
            ),
            dtype=uint8,
        )
        self.server.shutdown_event = self.shutdown_event
        self.create_thread(
            target=self.serve,
            name=f"mj_{name}",
            start=True,
        )

    @overrides
    def shutdown(self) -> None:
        self.log.i(
            f"Shutdown called for {self.__class__.__name__} / {self.name}",
            "shutdown",
        )
        self.server.shutdown()
        SandNode.shutdown(self)

    def push_neural_frame(self, _: Topic, boxes: SandBoxes) -> None:
        self.server.boxes = boxes

    def set_num_classes(self, _: Topic, num_classes: int) -> None:
        self.server.num_classes = num_classes

    @overrides
    def push_frame(self, frame: EnrichedFrame) -> None:
        self.server.frame = frame.frame

    def serve(self) -> None:
        self.set_thread_name(f"mj_{self.name}")
        self.server.serve_forever()
