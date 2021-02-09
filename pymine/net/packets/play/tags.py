"""Contains packets related to tags (https://wiki.vg/Protocol#Tags AND https://minecraft.gamepedia.com/Tag)."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer

from pymine.data.registries import BLOCK_REGISTRY, ITEM_REGISTRY, FLUID_REGISTRY, ENTITY_REGISTRY

__all__ = ("PlayTags",)


class PlayTags(Packet):
    """Sends ids to the client, see here: https://wiki.vg/Protocol#Tags. (Server -> Client)

    :param dict block: Block tags.
    :param dict item: Item tags.
    :param dict fluid: Fluid tags.
    :param dict entity: Entity tags.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar block:
    :ivar item:
    :ivar fluid:
    :ivar entity:
    """

    id = 0x5B
    to = 1

    def __init__(self, block: dict, item: dict, fluid: dict, entity: dict) -> None:
        super().__init__()

        # A tags list *should* be something like:
        # {
        #     identifier: {
        #         protocol_id: protocol id
        #     }
        # }

        self.block = block
        self.item = item
        self.fluid = fluid
        self.entity = entity

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
