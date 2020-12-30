"""Contains HandshakeHandshake, a packet for starting the connection between the server and client."""

from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('HandshakeHandshake',)


class HandshakeHandshake(Packet):
    """Initiates the connection between the server and client. (Client -> Server)

    :param int protocol: Protocol version to be used.
    :param str address: The host/address the client is connecting to.
    :param int port: The port the client is connection on.
    :param int next_state: The next state which the server should transfer to. 1 for status, 2 for login.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr protocol:
    :attr address:
    :attr port:
    :attr next_state:
    """

    id = 0x00
    to = 0

    def __init__(self, protocol: int, address: str, port: int, next_state: int) -> None:
        super().__init__()

        self.protocol = protocol
        self.address = address
        self.port = port
        self.next_state = next_state

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeHandshake:
        return cls(buf.unpack_varint(), buf.unpack_string(), buf.unpack('H'), buf.unpack_varint())
