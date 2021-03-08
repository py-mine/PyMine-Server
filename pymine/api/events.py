from pymine.api.abc import AbstractEvent, AbstractPlugin


class PacketEvent(AbstractEvent):
    def __init__(self, handler, state_id: int, packet_id: int):
        self.handler = handler
        self.cls = handler.__self__
        self.state_id = state_id
        self.packet_id = packet_id
