"""Contains packets related to players."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = ('PlayAcknowledgePlayerDigging',)


class PlayAcknowledgePlayerDigging(Packet):
    """Sent by server to acknowledge player digging. (Server -> Client)

    :param int x: The x coordinate of where the player is digging.
    :param int y: The y coordinate of where the player is digging.
    :param int z: The z coordinate of where the player is digging.
    :param int block: The block state id of the block that is being broken/dug.
    :param int status: Value 0-2 to denote whether player should start, cancel, or finish.
    :param bool successful: True if the block was dug successfully.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr block:
    :attr status:
    :attr successful:
    """

    id_ = 0x07
    to = 1

    def __init__(self, x: int, y: int, z: int, block: int, status: int, successful: bool) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.z = z
        self.block = block
        self.status = status
        self.successful = successful

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + \
            Buffer.pack_varint(self.block) + \
            Buffer.pack_varint(self.status) + \
            Buffer.pack_bool(self.successful)


class PlayDisconnect(Packet):
    """Sent by the server before it disconnects a client. The client assumes that the server has already closed the connection by the time the packet arrives.

    Clientbound(Server -> Client)"""

    id_ = 0x19
    to = 1

    def __init__(self, reason: Chat):
        self.reason = reason

    def encode(self):
        return Buffer.pack_chat(self.reason)


class PlayPlayerAbilitiesClientBound(Packet):
    """Defines the player's abilities. (Server -> Client)

    :param bytes flags: Client data bitfield, see here: https://wiki.vg/Protocol#Player_Abilities_.28clientbound.29.
    :param float flying_speed: Speed at which client is flying.
    :param float fov_modifier: FOV modifier value.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr flags:
    :attr flying_speed:
    :attr fov_modifier:
    """

    id_ = 0x30
    to = 1

    def __init__(self, flags: bytes, flying_speed: float, fov_modifier: float) -> None:
        super().__init__()

        self.flags = flags
        self.flying_speed = flying_speed
        self.fov_modifier = fov_modifier

    def encode(self) -> bytes:
        return self.flags + Buffer.pack('f', self.flying_speed) + \
            Buffer.pack('f', self.fov_modifier)


class PlayPlayerAbilitiesServerBound(Packet):
    """Tells the server whether the client is flying or not. (Client -> Server)

    :param bool flying: Whether player is flying or not.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr flying:
    """

    id_ = 0x1A
    to = 0

    def __init__(self, flying: bool) -> None:
        super().__init__()

        self.flying = flying

    def decode(self, buf: Buffer) -> PlayPlayerAbilitiesServerBound:
        return (buf.unpack('b') == 0x02)
