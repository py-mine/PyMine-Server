"""Contains packets related to tags (https://wiki.vg/Protocol#Tags AND https://minecraft.gamepedia.com/Tag)."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

from pymine.data.registries import BLOCK_REGISTRY, ITEM_REGISTRY, FLUID_REGISTRY, ENTITY_REGISTRY

__all__ = ("PlayTags",)


class PlayTags(Packet):
    """Sends ids to the client, see here: https://wiki.vg/Protocol#Tags. (Server -> Client)

    :param dict tags: All tags.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar block:
    :ivar item:
    :ivar fluid:
    :ivar entity:
    """

    id = 0x5B
    to = 1

    def __init__(self, tags: dict) -> None:
        super().__init__()

        # A tags list *should* be something like:
        # {
        #     identifier: {
        #         protocol_id: protocol id
        #     }
        # }

        self.block = tags["blocks"]
        self.item = tags["items"]
        self.fluid = tags["fluids"]
        self.entity = tags["entity_types"]

    def encode(self) -> bytes:
        out = b""

        for tags, REG in (
            (
                self.block,
                BLOCK_REGISTRY,
            ),
            (
                self.item,
                ITEM_REGISTRY,
            ),
            (
                self.fluid,
                FLUID_REGISTRY,
            ),
            (
                self.entity,
                ENTITY_REGISTRY,
            ),
        ):
            out += Buffer.pack_varint(len(tags))  # pack length

            for identifier in tags:
                # pack identifier name and  length of upcoming array
                out += Buffer.pack_string(identifier) + Buffer.pack_varint(len(tags[identifier]))

                for value in tags[identifier]:
                    # values should be encoded as varints, so we need their id
                    out += Buffer.pack_varint(REG.encode(value))

        return out
