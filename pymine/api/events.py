from pymine.api.abc import AbstractEvent, AbstractPlugin


class PacketEvent(AbstractEvent):
    def __init__(self, cls: AbstractPlugin, state_id: int, packet_id: int):
        self.cls = cls
        self.state_id = state_id
        self.packet_id = packet_id
