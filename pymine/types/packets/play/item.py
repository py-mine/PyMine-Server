"""Contains packets related to items."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = (
    'PlayUseItem',
    'PlayEditBook',
    'PlayPickItem',
    'PlayNameItem',
    'PlayHeldItemChangeServerBound',
    'PlayHeldItemChangeClientBound',
    'PlayCollectItem',
)


class PlayUseItem(Packet):
    """Sent by the client when the use item key is pressed. (Client -> Server)

    :param int hand: The hand used for the animation. main hand (0) or offhand (1).
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr hand:
    """

    id = 0x2F
    to = 0

    def __init__(self, hand: int) -> None:
        super().__init__()

        self.hand = hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayUseItem:
        return cls(buf.upack_varint())


class PlayEditBook(Packet):
    """Used by the client to edit a book. (Client -> Server)

    :param dict new_book: The new slot/data for the book.
    :param bool is_signing: Whether the player is signing the book or just saving a draft.
    :param int hand: The hand used. Either main hand (0) or offhand (1).
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr new_book:
    :attr is_signing:
    :attr hand:
    """

    id = 0x0C
    to = 0

    def __init__(self, new_book: dict, is_signing: bool, hand: int) -> None:
        super().__init__()

        self.new_book = new_book
        self.is_signing = is_signing
        self.hand = hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayEditBook:
        return cls(buf.unpack_slot(), buf.unpack('?'), buf.unpack_varint())


class PlayPickItem(Packet):
    """Used to swap out an empty space on the hotbar with the item in the given inventory slot. (Client -> Server)

    :param int slot_to_use: The slot to use.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr slot_to_use:
    """

    id = 0x18
    to = 0

    def __init__(self, slot_to_use: int) -> None:
        super().__init__()

        self.slot_to_use = slot_to_use

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPickItem:
        return cls(buf.unpack_varint())


class PlayNameItem(Packet):
    """Used by the client when renaming something in an anvil. (Client -> Server)

    :param str item_name: The new name of the item.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr item_name:
    """

    id = 0x20
    to = 0

    def __init__(self, item_name: str) -> None:
        super().__init__()

        self.item_name = item_name

    @classmethod
    def decode(cls, buf: Buffer) -> PlayNameItem:
        return cls(buf.unpack_string())


class PlayHeldItemChangeServerBound(Packet):
    """Sent when the player selects a new slot. (Client -> Server)

    :param int slot: The new selected slot.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr slot:
    """

    id = 0x25
    to = 0

    def __init__(self, slot: int) -> None:
        super().__init__()

        self.slot = slot

    @classmethod
    def decode(cls, buf: Buffer) -> PlayHeldItemChangeServerBound:
        return cls(buf.unpack('h'))


class PlayHeldItemChangeClientBound(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x3F
    to = 1

    def __init__(self, slot: int) -> None:
        super().init()

        self.slot = slot

    def encode(self) -> bytes:
        return Buffer.pack('h', self.slot)


class PlayCollectItem(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x55
    to = 1

    def __init__(self, collected_eid: int, collector_eid: int, item_count: int) -> None:
        super().__init__()

        self.collected_eid = collected_eid
        self.collector_eid = collector_eid
        self.item_count = item_count

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.collected_eid) + Buffer.pack_varint(self.collector_eid) + \
            Buffer.pack_varint(self.item_count)
