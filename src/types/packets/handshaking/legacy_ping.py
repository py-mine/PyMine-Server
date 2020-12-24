"""Contains packets that support the legacy server list ping protocol"""

from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('HandshakeLegacyPing_1', 'HandshakeLegacyPing_2',)


class HandshakeLegacyPingRequest(Packet):
    """Request from the client asking for legacy ping response. Client -> Server

    :param int protocol: Protocol version being used, should now always be 74/4a.
    :param str hostname: The host/address the client is connecting to.
    :param int port: The port the client is connection on.
    :attr type id_: Unique packet ID.
    :attr protocol:
    :attr hostname:
    :attr port:
    """

    id_ = 0xFE

    def __init__(self, protocol: int, hostname: str, port: int) -> None:
        super().__init__()

        self.protocol = protocol
        self.hostname = hostname
        self.port = port

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeLegacyPing_1:
        buf.read(15)
        return cls(buf.read(1), buf.read(buf.unpack('h')).decode('UTF-16BE'), buf.unpack('i'))


class HandshakeLegacyPingResponse(Packet):
    """Legacy response from the server to the client. Server -> Client

    :param str version: Version that the Minecraft server is running (i.e. 1.16.4).
    :param str motd: The server MOTD.
    :param int players_online: Amount of players currently on the server.
    :param int players_max: Maximum players allowed on the server.
    :attr type id_: Unique packet ID.
    :attr version:
    :attr motd:
    :attr players_online:
    :attr players_max:
    """

    id_ = 0xFF

    def __init__(self, version: str, motd: str, players_online: int, players_max: int) -> None:
        super().__init__()

        self.version = version
        self.motd = motd
        self.players_online = players_online
        self.players_max = players_max

    def encode(self) -> bytes:
        out_string = f'§1\x0074\x00{self.motd}\x00{self.players_online}\x00{self.players_max}'
        return b'\xff' + Buffer.pack('h', len(out_string)) + out_string.encode('UTF-16BE')
