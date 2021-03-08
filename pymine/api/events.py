import asyncio

from pymine.data.states import STATES


class Event:
    pass


class PacketEvent(Event):
    def __init__(self, state_id: int, packet_id: int):
        self.state_id = state_id
        self.packet_id = packet_id
