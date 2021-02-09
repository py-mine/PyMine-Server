from collections import OrderedDict
import aiofile
import os

from pymine.types.buffer import Buffer
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt

from pymine.data.default_nbt.level import new_level_nbt


class World:
    def __init__(self, server, name: str, path: str, chunk_cache_max: int) -> None:
        self.server = server

        self.name = name
        self.path = path  # should be "worlds/world_name_dim/" in production probably

        self.data = None

        self._chunk_cache_max = chunk_cache_max
        self._chunk_cache = OrderedDict()

        self._proper_name = None
        self._dimension = None

    @property
    def proper_name(self):
        if self._proper_name is None:
            self._proper_name = list(self.server.worlds.keys())[list(self.server.worlds.values()).index(self)]

        return self._proper_name

    @property
    def dimension(self):
        if self._dimension is None:
            self._dimension = "minecraft:" + self.proper_name.replace(self.name + "_", "")

        return self._dimension

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
            pass

        try:
            return self.cache_chunk(await self.server.chunkio.fetch_chunk_async(self.path, *key), key)
        except FileNotFoundError:
            chunk_data = self.server.generator.generate_chunk(self.data["RandomSeed"], self.dimension, chunk_x, chunk_z)
            return chunk_data
