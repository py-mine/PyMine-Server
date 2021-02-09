"""Contains packets related to resource packs."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = (
    "PlayResourcePackStatus",
    "PlayResourcePackSend",
)


class PlayResourcePackStatus(Packet):
    """Used by the client to send the status of whether a resource pack was loaded or not. (Client -> Server)

    :param int status: One of: successfully loaded (0), declined (1), failed download (2), accepted (3).
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar status:
    """

    id = 0x21
    to = 0

    def __init__(self, status: int) -> None:
        super().__init__()

        self.status = status

    @classmethod
    def decode(cls, buf: Buffer) -> PlayResourcePackStatus:
        return cls(buf.unpack_varint())


class PlayResourcePackSend(Packet):
    """Sends the url of the resource pack and hash of the resource pack file to the client. (Server -> Client)

    :param str url: The URL for the resource pack download.
    :param str hash_: 40 char, hexadecimal, lowercase, sha1 hash of the resource pack file.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar url:
    :ivar hash_:
    """

    id = 0x38
    to = 1

    def __init__(self, url: str, hash_: str) -> None:
        super().__init__()

        self.url = url
        self.hash_ = hash_

    def encode(self) -> bytes:
        return Buffer.pack_string(self.url) + Buffer.pack_string(self.hash_)
