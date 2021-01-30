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


def load_worlds(server, region_cache_max_per: int) -> dict:
    level_name = server.conf["level_name"]
    worlds = {}

    server.logger.info(f"Loading worlds for level {level_name}...")

    for ext in ("", "_nether", "_the_end"):
        name = level_name + ext
        worlds[name] = World(server, name, os.path.join("worlds", name), region_cache_max_per)

    server.logger.info(f'Loaded worlds: {", ".join(worlds.keys())}.')

    return worlds


class World:
    def __init__(self, server, world_name: str, world_path: str, region_cache_max: int) -> None:
        self.server = server

        self.world_name = world_name
        self.world_path = world_path  # should be "worlds/world_name_dim/" in production probably

        self.region_cache_max = region_cache_max
        self.region_cache = OrderedDict()

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
