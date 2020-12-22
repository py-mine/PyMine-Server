from __future__ import annotations
import secrets

from src.types.buffer import Buffer
from src.types.packet import Packet


class LoginStart(Packet):  # Client -> Server
    def __init__(self, username: str) -> None:
        super().__init__(0x00)

        self.username = username

    @classmethod
    def decode(cls, buf: Buffer) -> LoginStart:
        return LoginStart(buf.read(buf.unpack_varint()).decode('UTF-8'))


class LoginEncryptionRequest(Packet):  # Server -> Client
    def __init__(self, public_key: bytes) -> None:  # https://wiki.vg/Protocol#Encryption_Request
        self.public_key = public_key
        self.verify_token = secrets.token_bytes(16)

    def encode(self) -> bytes:
        return Buffer.pack_varint(20) + (' '*20).encode('UTF-8') + \
         Buffer.pack_varint(len(self.public_key)) + self.public_key + \
         Buffer.pack_varint(len(self.verify_token)) + self.verify_token
