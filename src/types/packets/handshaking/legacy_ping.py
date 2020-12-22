from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet
from src.types.packets.handshaking.handshaking import HandshakeHandshake
__all__ = ('HandshakeLegacyPing_1', 'HandshakeLegacyPing_2',)


class HandshakeLegacyPing_1(Packet):  # Client -> Server
    def __init__(self, protocol: int, hostname: str, port: int) -> None:
        super.__init__(0xFE)

        self.protocol = protocol
        self.hostname = hostname
        self.port = port

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeHandshake:
        buf.read(15)
        return cls(buf.read(1), buf.read(buf.unpack('h')).decode('UTF-16BE'), buf.unpack('i'))


class HandshakeLegacyPing_2(Packet):  # Server -> CLient
    def __init__(self, version: str, motd: str, players_online: int, players_max: int, protocol: int = 127) -> None:
        super.__init__(0xFF)

        self.protocol = protocol
        self.version = version
        self.motd = motd
        self.players_online = players_online
        self.players_max = players_max

    def encode(self) -> bytes:
        out_string = f'§1\x00{self.protocol}\x00{self.motd}\x00{self.players_online}\x00{self.players_max}'
        return b'\xff' + Buffer.pack('h', len(out_string)) + out_string.encode('UTF-16BE')
