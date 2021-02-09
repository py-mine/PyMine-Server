import aiofile
import struct
import zlib
import os

from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
from pymine.types.world import World
import pymine.types.nbt as nbt

from pymine.api.abc import AbstractChunkIO

# Setup world dict and load basic level data for each world
async def load_worlds(server, level_name: str, chunk_cache_max_per: int) -> dict:
    worlds = {}

    server.logger.info(f"Loading default worlds for level {level_name}...")

    # Worlds, in the world dict (server.worlds) are indexed by their dimension type, this, however can change in the future
    # worlds are passed their file name / folder name (i.e. level_name + ext) via their constructors
    # their proper name is just their dimension type, like overworld.
    # Worlds must be .init()ed, this loads their level.dat data and maybe other stuff later
    for ext, proper_name in zip(("", "_nether", "_the_end"), ("overworld", "nether", "the_end")):
        name = level_name + ext
        worlds[f"minecraft:{proper_name}"] = await World(
            server, name, os.path.join("worlds", name), chunk_cache_max_per
        ).init()

    server.logger.info(f'Loaded default worlds: {", ".join([w.name for w in worlds.values()])}.')

    return worlds


class ChunkIO(AbstractChunkIO):
    @staticmethod
    def calc_offset(chunk_x: int, chunk_z: int) -> int:
        return 4 * ((chunk_x & 31) + (chunk_z & 31) * 32)

    @staticmethod
    def find_chunk(location: int) -> tuple:
        offset = (location >> 8) & 0xFFFFFF
        size = location & 0xFF

        return offset * 4096, size * 4096

    @classmethod
    def fetch_chunk(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        rx, ry = chunk_x // 32, chunk_z // 32
        region_path = os.path.join(world_path, "region", f"r.{rx}.{ry}.mca")

        if not os.path.isfile(region_path):
            raise FileNotFoundError(region_path)

        loc_table_loc = cls.calc_offset(chunk_x, chunk_z)

        with open(region_path, "rb") as region_file:
            region_file.seek(loc_table_loc)

            offset, length = cls.find_chunk(region_file.read(4))

            region_file.seek(loc_table_loc + 4096)
            timestamp = struct.unpack(">i", region_file.read(4))

            region_file.seek(offset + 5)
            return Chunk(nbt.TAG_Compound.unpack(Buffer(zlib.decompress(region_file.read(length - 5)))), timestamp)

    @classmethod
    async def fetch_chunk_async(cls, world_path: str, chunk_x: int, chunk_z: int) -> Chunk:
        rx, ry = chunk_x // 32, chunk_z // 32
        region_path = os.path.join(world_path, "region", f"r.{rx}.{ry}.mca")

        if not os.path.isfile(region_path):
            raise FileNotFoundError(region_path)

        loc_table_loc = cls.calc_offset(chunk_x, chunk_z)

        async with aiofile.async_open(region_path, "rb") as region_file:
            region_file.seek(loc_table_loc)

            offset, length = cls.find_chunk(await region_file.read(4))

            region_file.seek(loc_table_loc + 4096)
            timestamp = struct.unpack(">i", await region_file.read(4))

            region_file.seek(offset + 5)
            return Chunk(nbt.TAG_Compound.unpack(Buffer(zlib.decompress(await region_file.read(length - 5)))), timestamp)
