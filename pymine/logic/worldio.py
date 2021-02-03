import os

from pymine.types.world import World


async def load_worlds(server, level_name: str, region_cache_max_per: int) -> dict:
    worlds = {}

    server.logger.info(f"Loading worlds for level {level_name}...")

    for ext in ("", "_nether", "_the_end"):
        name = level_name + ext
        worlds[name] = await World(server, name, os.path.join("worlds", name), region_cache_max_per).init()

    worlds["overworld"], worlds["nether"], worlds["the_end"] = worlds.values()

    server.logger.info(f'Loaded default worlds: {", ".join(worlds.keys())}.')

    return worlds
