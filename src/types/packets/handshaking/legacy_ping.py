from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('HandshakeLegacyPing',)

class HandshakeLegacyPing_1(Packet):  # Client -> Server
    def __init__(self, protocol: int, hostname: str, port: int):
        super.__init__(-0x1)

        self.protocol = protocol
        self.hostname = hostname
        self.port = port

    @classmethod
    def decode(cls, buf: Buffer) -> HandshakeHandshake:
        buf.read(15)
        return cls(buf.read(1), buf.read(buf.unpack('h')).decode('UTF-16BE'), buf.unpack('i'))

class HandshakeLegacyPing_2(Packet):  # Server -> CLient
    def __init__(self, protocol: int = 127, version: str, motd: str, player_count: int, max_players: int):
        super.__init__(-0x1)

        self.protocol = protocol
        self.version = version
        self.motd = motd
        self.player_count = player_count
        self.max_players = max_players

    def encode(self):
        out_string = f'§1\x00{self.protocol}\x00{self.motd}\x00{self.player_count}\x00{self.max_players}'
        return b'\xff' + Buffer.pack('h', len(out_string)) + out_string.encode('UTF-16BE')
