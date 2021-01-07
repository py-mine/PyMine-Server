"""Contains packets relating to chunks."""

from __future__ import annotations
from nbt import nbt

from src.types.packet import Packet
from src.types.buffer import Buffer

__all__ = ('PlayUnloadChunk', 'PlayUpdateLight',)


class PlayUnloadChunk(Packet):
    """Tells the client to unload a chunk column. Clientbound(Server => Client)"""

    id = 0x1C
    to = 1

    def __init__(self, chunk_x: int, chunk_z: int) -> None:
        super().__init__()

        self.chunk_x, self.chunk_z = chunk_x, chunk_z

    def encode(self) -> bytes:
        return Buffer.pack('i', self.chunk_x) + Buffer.pack('i', self.chunk_z)


class PlayChunkData(Packet):
    """Sends chunk data to the client. (Server -> Client)

    :param int chunk_x: The chunk x coordinate (block x coordinate // 16).
    :param int chunk_z: The chunk z coordinate (block z coordinate // 16).
    :param bool full_chunk: See here: https://wiki.vg/Chunk_Format#Full_chunk.
    :param int prim_bit_mask: Bitmask with bits set to 1 for every 16×16×16 chunk section whose data is included in Data. The least significant bit represents the chunk section at the bottom of the chunk column (from y=0 to y=15).
    :param nbt.TAG heightmaps: Compound containing one long array named MOTION_BLOCKING, which is a heightmap for the highest solid block at each position in the chunk (as a compacted long array with 256 entries at 9 bits per entry totaling 36 longs). The Notchian server also adds a WORLD_SURFACE long array, the purpose of which is unknown, but it's not required for the chunk to be accepted.
    :param bytes data: See chunk data format: https://wiki.vg/Chunk_Format#Full_chunk.
    :param list block_entities: Array of nbt.TAGs.
    :param int biomes: Unknown, see here: https://wiki.vg/Protocol#Chunk_Data.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr chunk_x:
    :attr chunk_z:
    :attr full_chunk:
    :attr prim_bit_mask:
    :attr heightmaps:
    :attr data:
    :attr block_entities:
    :attr biomes:
    """

    id = 0x20
    to = 1

    def __init__(
            self,
            chunk_x: int,
            chunk_z: int,
            full_chunk: bool,
            prim_bit_mask: int,
            heightmaps: nbt.TAG,
            data: bytes,
            block_entities: list,
            biomes: int = None) -> None:
        super().__init__()

        self.chunk_x, self.chunk_z = chunk_x, chunk_z
        self.full_chunk = full_chunk
        self.prim_bit_mask = prim_bit_mask
        self.heightmaps = heightmaps
        self.data = data
        self.block_entities = block_entities
        self.biomes = biomes

    def encode(self) -> bytes:
        raise NotImplementedError


class PlayUpdateLight(Packet):
    """Updates light levels for a chunk."""

    id = 0x23
    to = 1

    def __init__(
            self,
            chunk_x: int,
            chunk_z: int,
            trust_edges: bool,
            sky_light_mask: int,
            block_light_mask: int,
            empty_sky_light_mask: int,
            empty_block_light_mask: int,
            sky_light_array: list,
            block_light_array: list) -> None:
        super().__init__()

        self.chunk_x, self.chunk_z = chunk_x, chunk_z
        self.trust_edges = trust_edges
        self.sky_light_mask, self.empty_sky_light_mask = sky_light_mask, empty_sky_light_mask
        self.block_light_mask, self.empty_block_light_mask = block_light_mask, empty_block_light_mask
        self.sky_light_array = sky_light_array
        self.block_light_array = block_light_array

    def encode(self) -> bytes:
        return Buffer.pack('i', self.chunk_x) + Buffer.pack('i', self.chunk_z) + Buffer.pack('?', self.trust_edges) + \
            Buffer.pack_varint(self.sky_light_mask) + Buffer.pack_varint(self.block_light_mask) + \
            Buffer.pack_varint(self.empty_sky_light_max) + Buffer.pack_varint(self.empty_block_light_mask) + \
            Buffer.pack_array('c', self.sky_light_array) + Buffer.pack_array('c', self.block_light_array)
