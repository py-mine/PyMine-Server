from __future__ import annotations

from src.types.buffer import Buffer

__all__ = ('Packet', 'PacketClientboundJSON',)


class Packet:
    """Base Packet class.

    :param int id: Packet identifaction number. Defaults to -0x1.
    :attr id:
    """

    id_ = None

    def __init__(self, id_: int = None) -> None:
        if id_ is None:
            self.id_ = self.__class__.id_
        else:
            self.id_ = id_
            self.__class__.id_ = id_


class PacketClientboundJSON(Packet):
    """Base class used in most client-bound play packets."""

    id_ = None

    def __init__(self, id_: int):
        super().__init__()

    def encode(self):
        return Buffer.pack_json(self.response_data)  # assumes response_data is present
