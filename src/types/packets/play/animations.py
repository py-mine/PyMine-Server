"""Contains animation packets."""

from __future__ import annotations

from src.types.packet import PacketClientboundJSON

__all__ = ('PlayEntityAnimation',)


class PlayEntityAnimation(PacketClientboundJSON):
    """Sent whenever an entity should change animation. Client bound(Client -> Server)."""

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x05)


class PlayBlockBreakAnimation(PacketClientboundJSON):
    """0–9 are the displayable destroy stages and each other number means that there is no animation on this coordinate.
     Client bound(Client -> Server)."""
    # Block break animations can still be applied on air; the animation will remain visible although there is no block being broken.
    # However, if this is applied to a transparent block, odd graphical effects may happen, including water losing its transparency.
    # An effect similar to this can be seen in normal gameplay when breaking ice blocks
    # If you need to display several break animations at the same time you have to give each of them a unique Entity ID.
    # The entity ID does not need to correspond to an actual entity on the client. It is valid to use a randomly generated number.

    def __init__(self, response_data: dict) -> None:
        super().__init__(0x08)
