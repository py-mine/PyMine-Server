from collections import OrderedDict
import aiofile
import os

from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt

from pymine.data.default_nbt.level import new_level_nbt


def block_to_chunk_coords(block_x: int, block_z: int) -> tuple:
    return block_x // 16, block_z // 16


def chunk_to_block_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x * 16, chunk_z * 16


def chunk_to_region_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x // 32, chunk_z // 32


def region_file_name(region_x: int, region_z: int) -> str:  # Gens the name for the region file in the format r.x.y.mca
    return ".".join(("r", str(region_x), str(region_z), "mca"))


class World:
    def __init__(self, server, name: str, path: str, chunk_cache_max: int) -> None:
        self.server = server

        self.name = name
        self.path = path  # should be "worlds/world_name_dim/" in production probably

        self.data = None

        self._chunk_cache_max = chunk_cache_max
        self._chunk_cache = OrderedDict()

    async def init(self):
        self.data = await self.load_level_data()
        return self  # for fluent style chaining

    async def load_level_data(self):
        file = os.path.join(self.path, "level.dat")

        if os.path.isfile(file):
            async with aiofile.async_open(file, "rb") as level_data_file:
                return nbt.TAG_Compound.unpack(Buffer(await level_data_file.read()))

        return new_level_nbt((2586, self.server.meta.version, 19133), self.name, (0, 100, 0), self.server.conf["seed"])["Data"]

    def cache_chunk(self, chunk: Chunk, key: tuple) -> Chunk:
        self._chunk_cache[key] = chunk

        if len(self.chunk_cache) > self._chunk_cache_max:
            self._chunk_cache.popitem(False)

        return chunk

    async def fetch_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        key = (chunk_x, chunk_z)

        try:
            return self._chunk_cache[key]
        except KeyError:
            return self.cache_chunk(await self.server.chunkio.fetch_chunk_async(self.path, *key), key)
