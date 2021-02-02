from collections import OrderedDict
import aiofile
import os

from pymine.types.level import LevelData
from pymine.types.buffer import Buffer
from pymine.types.region import Region
from pymine.types.chunk import Chunk
import pymine.types.nbt as nbt


def block_to_chunk_coords(block_x: int, block_z: int) -> tuple:
    return block_x // 16, block_z // 16


def chunk_to_block_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x * 16, chunk_z * 16


def chunk_to_region_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x // 32, chunk_z // 32


def region_file_name(region_x: int, region_z: int) -> str:
    return ".".join(("r", str(region_x), str(region_z), "mca"))


class World:
    def __init__(self, name: str, path: str, region_cache_max: int) -> None:
        self.name = name
        self.path = path  # should be "worlds/world_name_dim/" in production probably

        self.data = None

        self.region_cache_max = region_cache_max
        self.region_cache = OrderedDict()

    async def init(self):
        level_file_path = os.path.join(self.path, "level.dat")

        if not os.path.isfile(level_file_path):
            raise NotImplementedError

        self.data = await LevelData.from_file(level_file_path)

        return self  # for fluent style chaining

    def cache_region(self, region: Region, key: tuple) -> Region:
        self.region_cache[key] = region

        if len(self.region_cache) > self.region_cache_max:
            self.region_cache.popitem(False)

        return region

    async def fetch_region(self, region_coords: tuple) -> Region:
        try:
            self.region_cache.move_to_end(region_coords)
            return self.region_cache[region_coords]
        except KeyError:
            file = os.path.join(self.world_path, "region", region_file_name(*region_coords))
            return self.cache_region(await Region.from_file(file), region_coords)

    async def fetch_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        region = await self.fetch_region(chunk_to_region_coords(chunk_x, chunk_z))

        try:
            return region[chunk_x, chunk_z]
        except KeyError:
            raise NotImplementedError("Nice try bucko, but world gen hasn't been implemented yet...")
