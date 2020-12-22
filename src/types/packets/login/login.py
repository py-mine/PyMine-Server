from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet


class LoginStart(Packet):  # Client -> Server
    def __init__(self, username: str):
        super().__init__(0x00)

        self.username = username

    @classmethod
    def decode(cls, buf: Buffer) -> LoginStart:
        return LoginStart(buf.read(buf.unpack_varint()).decode('UTF-8'))
