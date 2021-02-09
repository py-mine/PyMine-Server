"""Contains packets relating to plugin channels and messages. See here: https://wiki.vg/Plugin_channels"""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

__all__ = ("PlayPluginMessageClientBound", "PlayPluginMessageServerBound")


class PlayPluginMessageClientBound(Packet):
    """Used to send a "plugin message". See here https://wiki.vg/Protocol#Plugin_Message_.28serverbound.29 (Server -> Client)

    :param str channel: The plugin channel to be used.
    :param bytes data: Data to be sent to the client.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar data:
    """

    id = 0x17
    to = 1

    def __init__(self, channel: str, data: bytes) -> None:
        super().__init__()

        self.channel = channel
        self.data = data

    def encode(self) -> bytes:
        return Buffer.pack_string(self.channel) + self.data


class PlayPluginMessageServerBound(Packet):
    """Used to send plugin data to the server (Client -> Server)

    :param str channel: The plugin channel being used.
    :param bytes data: Data to be sent to the client.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar data:
    """

    id = 0x0B
    to = 0

    def __init__(self, channel: str, data: bytes) -> None:
        super().__init__()

        self.channel = channel
        self.data = data

    def decode(self, buf: Buffer) -> PlayPluginMessageServerBound:
        return PlayPluginMessageServerBound(buf.unpack_string(), Buffer(buf.read()))
