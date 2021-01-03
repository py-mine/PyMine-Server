from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayKeepAliveClientBound' ,)
 class PlayKeepAliveClientBound(Packet):
     """The server will frequently send out a keep-alive, each containing a random ID. The client must respond with the same packet. If the client does not respond to them for over 30 seconds, the server kicks the client. Vice versa, if the server does not send any keep-alives for 20 seconds, the client will disconnect and yields a "Timed out" exception. """
     id = 0x1F
     to = 1
    def __init__(self, keep_alive_id: int):
        self.keep_alive_id = keep_alive_id
    def encode(self):
        return Buffer.pack('l', self.keep_alive_id)
