"""Contains packets related to items."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUseItem', 'PlayEditBook',)


class PlayUseItem(Packet):
    """Sent by the client when the use item key is pressed. (Client -> Server)

    :param int hand: The hand used for the animation. main hand (0) or offhand (1).
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
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
    :attr type id: Unique packet ID.
    :attr type to: Packet direction.
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
        return cls(buf.unpack_slot(), buf.unpack_bool(), buf.unpack_varint())
