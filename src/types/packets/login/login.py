"""Contains packets relating to client logins"""

from __future__ import annotations
import secrets
import uuid

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = (
    'LoginStart',
    'LoginEncryptionRequest',
    'LoginEncryptionResponse',
    'LoginSuccess',
)


class LoginStart(Packet):  # Client -> Server
    """Packet from client asking to start login process"""

    id_ = 0x00

    def __init__(self, username: str) -> None:
        super().__init__()

        self.username = username

    @classmethod
    def decode(cls, buf: Buffer) -> LoginStart:
        return LoginStart(buf.read(buf.unpack_varint()).decode('UTF-8'))


class LoginEncryptionRequest(Packet):  # Server -> Client
    """Used by the server to ask the client to encrypt the login process"""

    id_ = 0x01

    def __init__(self, public_key: bytes) -> None:  # https://wiki.vg/Protocol#Encryption_Request
        super().__init__()

        self.public_key = public_key
        self.verify_token = secrets.token_bytes(16)

    def encode(self) -> bytes:
        return Buffer.pack_string(' '*20) + \
         Buffer.pack_varint(len(self.public_key)) + self.public_key + \
         Buffer.pack_varint(len(self.verify_token)) + self.verify_token


class LoginEncryptionResponse(Packet):  # Client -> Server
    """Response from the client to a LoginEncryptionRequest"""

    id_ = 0x01

    def __init__(self, shared_key: bytes, verify_token: bytes) -> None:
        super().__init__()

        self.shared_key = shared_key
        self.verify_token = verify_token

    @classmethod
    def decode(cls, buf: Buffer) -> LoginEncryptionResponse:
        return LoginEncryptionResponse(buf.read(buf.unpack_varint()), buf.read(buf.unpack_varint()))


class LoginSuccess(Packet):  # Server -> Client
    """Sent by the server to denote a successfull login"""

    id_ = 0x02

    def __init__(self, uuid: uuid.UUID, username: str) -> None:
        super().__init__()

        self.uuid = uuid
        self.username = username

    def encode(self):
        return Buffer.pack_uuid(self.uuid) + Buffer.pack_string(username)
