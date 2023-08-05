from __future__ import annotations

from abc import abstractmethod
from datetime import datetime

from overrides import EnforceOverrides

from sand.datatypes import (
    CollisionMap,
    EnrichedFrame,
    EnrichedLidarPacket,
    Image,
    LidarPacket,
)
from sand.datatypes.aerialmap import AerialMap


class ReaderSubscriber(EnforceOverrides):
    @abstractmethod
    def push_image(self, frame: Image, stream_name: str) -> None:
        """
        A method where the frame from a CameraReader is pushed to a ReaderSubscriber.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Reader-thread.
        """


class EnrichedSubscriber(EnforceOverrides):
    @abstractmethod
    def push_frame(self, frame: EnrichedFrame) -> None:
        """
        A method where the enriched frame from a FrameEnricher is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.
        """


class LidarSubscriber(EnforceOverrides):
    @abstractmethod
    def push_packet(self, packet: LidarPacket) -> None:
        """
        A method where a udp packet from a vlp16 capture is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-capture-thread.
        """


class EnrichedLidarSubscriber(EnforceOverrides):
    @abstractmethod
    def push_enriched_packet(self, packet: EnrichedLidarPacket) -> None:
        """
        A method where a udp packet from a vlp16 capture is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-capture-thread.
        """


class NeuralNetInterestingSubscriber(EnforceOverrides):
    @abstractmethod
    def set_interesting(self, timestamp: datetime) -> None:
        """
        A method where the NN tells its subscribers, that there was something interesting
        on the recording at {timestamp}.

        Important here is that this method should be as short as possible. As it is a synchronous method to avoid
        ordering and dirty-write situations.
        """

    @abstractmethod
    def push_neural_frame(self, frame: EnrichedFrame) -> None:
        """
        A method where the enriched frame from a FrameEnricher is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.
        """


class ImageTransformerSubscriber(EnforceOverrides):
    @abstractmethod
    def push_transformed_frame(self, frame: EnrichedFrame) -> None:
        """A method where the enriched frame from an ImageTransformer is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.

        Frame is guaranteed to have a transformed image.
        """


class CraneMapSubscriber(EnforceOverrides):
    @abstractmethod
    def push_map(self, crane_map: AerialMap) -> None:
        """
        A method where the enriched frame from a FrameEnricher is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.
        """


class BoxTransformerSubscriber(EnforceOverrides):
    @abstractmethod
    def push_box_frame(self, frame: EnrichedFrame) -> None:
        """
        A method where the enriched frame from a FrameEnricher is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.
        """


class SensorFusionSubscriber(EnforceOverrides):
    @abstractmethod
    def push_fusion_map(self, collision_map: CollisionMap, status: bool) -> None:
        """
        A method where the colission map from the sensor fusion is pushed.

        Important here is that this method should be as short as possible. We
        recommend a Producer-Consumer-like implementation, as the 'push' is
        happening on the main-Enricher-thread.
        """
