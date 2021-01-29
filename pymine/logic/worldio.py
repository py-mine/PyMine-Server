from collections import OrderedDict
import os

from pymine.types.buffer import Buffer
from pymine.types.region import Region
from pymine.types.chunk import Chunk


def block_to_chunk_coords(block_x: int, block_z: int) -> tuple:
    return block_x // 16, block_z // 16


def chunk_to_block_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x * 16, chunk_z * 16


def chunk_to_region_coords(chunk_x: int, chunk_z: int) -> tuple:
    return chunk_x // 32, chunk_z // 32


def region_file_name(region_x: int, region_z: int) -> str:
    return ".".join(("r", str(region_x), str(region_z), "mca"))


class WorldIO:
    def __init__(self, server, world_name: str, region_cache_max: int) -> None:
        self.server = server

        self.world_name = world_name

        self.region_cache_max = region_cache_max
        self.region_cache = OrderedDict()

    def cache_region(self, region: Region, key: tuple) -> Region:
        self.region_cache[key] = region

        if len(region_cache) > self.region_cache_max:
            self.region_cache.popitem(False)

        return region

    async def fetch_region(self, chunk_x: int, chunk_z: int) -> Region:
        if not os.path.isdir(file):
            raise NotImplementedError("Region file doesn't exist (and worldgen hasn't been done yet...)")

        key = chunk_to_region_coords(chunk_x, chunk_z)

        try:
            self.region_cache.move_to_end(key)
            return self.region_cache[key]
        except KeyError:
            return self.cache_region(await Region.from_file(file), key)

    def fetch_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        raise NotImplementedError
