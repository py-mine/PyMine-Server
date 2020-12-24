"""Contains packets related to entitys."""

from __future__ import annotations

from src.types.packet import PacketClientboundJSON

__all__ = ('PlayBlockAction', "PlayBlockChange")


class PlayBlockAction(PacketClientboundJSON):
    """This packet is used for a number of actions and animations performed by blocks, usually non-persistent.
    Client bound(Client -> Server).
    """

    id_ = 0x0A

    def __init__(self, response_data: dict) -> None:
        super().__init__()


class PlayBlockChange(PacketClientboundJSON):
    """Fired when a block is changed within the render distance. Client bound(Client -> Server)."""

    id_ = 0x0B

    def __init__(self, response_data: dict) -> None:
        super().__init__()
