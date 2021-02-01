import os

from pymine.types.world import World


async def load_worlds(logger, level_name: str, region_cache_max_per: int) -> dict:
    worlds = {}

    logger.info(f"Loading worlds for level {level_name}...")

    for ext in ("", "_nether", "_the_end"):
        name = level_name + ext
        worlds[name] = await World(name, os.path.join("worlds", name), region_cache_max_per).init()

    logger.info(f'Loaded worlds: {", ".join(worlds.keys())}.')

    return worlds
