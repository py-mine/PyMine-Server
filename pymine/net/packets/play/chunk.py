"""Contains packets relating to chunks."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt

__all__ = (
    "PlayUnloadChunk",
    "PlayChunkData",
    "PlayUpdateLight",
)


class PlayUnloadChunk(Packet):
    """Tells the client to unload a chunk column. Clientbound(Server => Client)"""

    id = 0x1C
    to = 1

    def __init__(self, chunk_x: int, chunk_z: int) -> None:
        super().__init__()

        self.chunk_x, self.chunk_z = chunk_x, chunk_z

    def encode(self) -> bytes:
        return Buffer.pack("i", self.chunk_x) + Buffer.pack("i", self.chunk_z)


class PlayChunkData(Packet):
    """Sends a chunk / its data to the client. (Server -> Client)

    :param Chunk chunk: The chunk to send the data for.
    :param bool full: Whether the chunk is "full" or not, see here: https://wiki.vg/Chunk_Format#Full_chunk
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar chunk:
    :ivar full:
    """

    id = 0x20
    to = 1

    def __init__(self, chunk: Chunk, full: bool) -> None:
        super().__init__()

        self.chunk = chunk
        self.full = full

    def encode(self) -> bytes:
        out = Buffer.pack("i", self.chunk.x) + Buffer.pack("i", self.chunk.z) + Buffer.pack("?", self.full)

        mask = 0
        chunk_sections_buffer = Buffer()

        for y, section in self.chunk.sections.items():  # pack chunk columns into buffer and generate a bitmask
            if y >= 0:
                mask |= 1 << y
                chunk_sections_buffer.write(Buffer.pack_chunk_section(section))

        out += Buffer.pack_varint(mask) + Buffer.pack_nbt(
            nbt.TAG_Compound("", [self.chunk["Heightmaps"]["MOTION_BLOCKING"], self.chunk["Heightmaps"]["WORLD_SURFACE"]])
        )

        if self.full:
            out += Buffer.pack_varint(len(Chunk["Biomes"])) + b"".join([Buffer.pack_varint(n) for n in Chunk["Biomes"]])

        out += len(chunk_sections_buffer) + chunk_sections_buffer.read()

        # here we would pack the block entities, but we don't support them yet so we just send an array with length of 0
        out += Buffer.pack_varint(0)

        return out


class PlayUpdateLight(Packet):
    """Updates light levels for a chunk."""

    id = 0x23
    to = 1

    def __init__(self, chunk: Chunk) -> None:
        super().__init__()

        self.chunk = chunk

    def encode(self) -> bytes:
        out = Buffer.pack_varint(self.chunk.x) + Buffer.pack_varint(self.chunk.z) + Buffer.pack('?', True)

        sky_light_mask = 0
        block_light_mask = 0
        empty_sky_light_mask = 0
        empty_block_light_mask = 0

        for y, section in chunk.sections.items():
            if y >= 0:
                if section.sky_light is not None:
                    if len(section.sky_light.nonzero()) == 0:
                        empty_sky_light_mask |= 1 << y
                    else:
                        sky_light_mask |= 1 << y

                if section.block_light is not None:
                    if len(section.block_light.nonzero()) == 0:
                        empty_block_light_mask |= 1 << y
                    else:
                        block_light_mask |= 1 << y
