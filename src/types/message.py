from __future__ import annotations

from src.types.packet import Packet

class Message:
    """
    A Minecraft chat message
    """

    def __init__(self, message):
        self.message = message

    @classmethod
    def from_packet(cls, packet: Packet) -> object:
        return cls(packet.unpack_json())

    def to_bytes(self):
        return Packet.pack_json(self.value)

    @classmethod
    def from_string(cls, text):
        pass
