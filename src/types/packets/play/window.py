
"""Contains packets related to windows."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayWindowConfirmation', 'PlayCloseWindow', 'PlayWindowProperty',)


class PlayWindowConfirmation(Packet):
    """A packet indicating whether a request from the client was accepted or if there was a problem.
    Server -> Client"""

    id = 0x11
    to = 1

    def __init__(self, window_id: int, action_number: int, accepted: bool) -> None:
        super().__init__()

        self.window_id = window_id
        self.action_number = action_number
        self.accepted = accepted

    def encode(self) -> bytes:
        return Buffer.pack('b', self.window_id) + Buffer.pack('h', self.action_number) + \
            Buffer.pack_bool(self.accepted)


class PlayCloseWindow(Packet):
    """This packet is sent from the server to the client when a window is forcibly closed, such as when a chest is destroyed while it's open. """

    id = 0x12
    to = 1

    def __init__(self, window_id: int):
        super().__init__()

        self.window_id = window_id

    def encode(self):
        return Buffer.pack('B', self.window_id)


class PlayWindowProperty(Packet):
    """This packet is used to inform the client that part of a GUI window should be updated. ClientboundServer -> Client"""

    id = 0x14
    to = 1

    def __init__(self, window_id: int, property: int, value: int):
        super().__init__()

        self.window_id = window_id
        self.property = property
        self.value = value

    def encode(self):
        return Buffer.pack('B', self.window_id) + Buffer.pack('h', self.property) +\
            Buffer.pack('h', self.value)
