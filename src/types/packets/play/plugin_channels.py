from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayPluginMessageClientBound',)


class PlayPluginMessageClientBound(Packet):
    """Used to send a "plugin message". See here https://wiki.vg/Protocol#Plugin_Message_.28serverbound.29 (Server -> Client)

    :param bytes data: Data to be sent to the client.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr data:
    """

    id_ = 0x17
    to = 1

    def __init__(self, data: bytes) -> None:
        super().__init__()

        self.data = data

    def encode(self) -> bytes:
        return data


# class PlayPluginMessageServerBound(Packet):
#
#     id_ = 0x0B
#     to = 0
#
#     def __init__(self, data: bytes) -> None:
#         super().__init__()
#
#         self.data = data
#
#     def decode(self, buf: Buffer) -> PlayPluginMessageServerBound:
#         raise NotImplementedError
