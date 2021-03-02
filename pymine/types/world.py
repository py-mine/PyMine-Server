from collections import OrderedDict
import aiofile
import time
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

        self.data = None  # data from the level.dat

        self._chunk_cache_max = chunk_cache_max
        self._chunk_cache = OrderedDict()

        self._cached_name = None

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default

    @property
    def cached_name(self):
        if self._cached_name is None:
            self._cached_name = list(self.server.worlds.keys())[list(self.server.worlds.values()).index(self)]

        return self._cached_name

    async def init(self):
        self.data = await self.load_level_data()
        return self  # for fluent style chaining

    # loads the level.dat for the current world
    async def load_level_data(self):
        file = os.path.join(self.path, "level.dat")

        if os.path.isfile(file):
            async with aiofile.async_open(file, "rb") as level_data_file:
                return nbt.TAG_Compound.unpack(Buffer(await level_data_file.read()))

        return new_level_nbt((2586, self.server.meta.version, 19133), self.name, (0, 100, 0), self.server.conf["seed"])["Data"]

    # caches a chunk and returns sed chunk
    def cache_chunk(self, chunk: Chunk, key: tuple) -> Chunk:
        self._chunk_cache[key] = chunk

        if len(self._chunk_cache) > self._chunk_cache_max:
            self._chunk_cache.popitem(False)

        return chunk

    async def fetch_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        key = (chunk_x, chunk_z)

        try:  # try to fetch chunk from cache
            return self._chunk_cache[key]
        except KeyError:
            pass

        try:  # try to fetch from disk
            return self.cache_chunk(await self.server.chunkio.fetch_chunk_async(self.path, *key), key)
        except FileNotFoundError:  # fall back to generate chunk
            return self.cache_chunk(
                self.server.generator.generate_chunk(self.data["RandomSeed"].data, self.cached_name, chunk_x, chunk_z), key
            )
