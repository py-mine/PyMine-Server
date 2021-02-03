import os

from pymine.types.world import World


async def load_worlds(server, level_name: str, region_cache_max_per: int) -> dict:
    worlds = {}

    server.logger.info(f"Loading worlds for level {level_name}...")

    for ext, proper_name in zip(("", "_nether", "_the_end"), ("overworld", "nether", "the_end")):
        name = level_name + ext
        worlds[proper_name] = await World(server, name, os.path.join("worlds", name), region_cache_max_per).init()

    server.logger.info(f'Loaded default worlds: {", ".join([w.name for w in worlds.values()])}.')

    return worlds
