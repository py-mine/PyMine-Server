"""Contains packets for maintaining the connection between client and server."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ('PlayKeepAliveClientBound', 'PlayKeepAliveServerBound',)


class PlayKeepAliveClientBound(Packet):
    """Sent by the server in order to maintain connection with the client. (Server -> Client)

    :param int keep_alive_id: A randomly generated (by the server) integer/long.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr keep_alive_id:
    """

    id = 0x1F
    to = 1

    def __init__(self, keep_alive_id: int) -> None:
        super().__init__()

        self.keep_alive_id = keep_alive_id

    def encode(self) -> bytes:
        return Buffer.pack('q', self.keep_alive_id)


class PlayKeepAliveServerBound(Packet):
    """Sent by client in order to maintain connection with server. (Client -> Server)

    :param int keep_alive_id: A randomly generated (by the server) integer/long.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr keep_alive_id:
    """

    id = 0x10
    to = 0

    def __init__(self, keep_alive_id: int) -> None:
        super().__init__()

        self.keep_alive_id = keep_alive_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayKeepAliveServerBound:
        return cls(buf.unpack('q'))
