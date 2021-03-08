from pymine.api.abc import AbstractEvent

class PacketEvent(AbstractEvent):
    def __init__(self, state_id: int, packet_id: int):
        self.state_id = state_id
        self.packet_id = packet_id
