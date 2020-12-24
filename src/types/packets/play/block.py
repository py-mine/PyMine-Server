"""Contains packets related to entitys."""

from __future__ import annotations

from src.types.base import PacketClientboundJSON


__all__ = ('PlayBlockAction',)


class PlayBlockAction(PacketClientboundJSON):
    """This packet is used for a number of actions and animations performed by blocks, usually non-persistent.
    Client bound(Client -> Server).
    """

    def __init__(self, response_data: dict) -> None:
        super.__init__(0x0A)
