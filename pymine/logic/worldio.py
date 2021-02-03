import os

from pymine.types.world import World


async def load_worlds(server, level_name: str, region_cache_max_per: int) -> dict:
    worlds = {}

    server.logger.info(f"Loading default worlds for level {level_name}...")

    # Worlds, in the world dict (server.worlds) are indexed by their dimension type, this, however can change in the future
    # worlds are passed their file name / folder name (i.e. level_name + ext) via their constructors
    # their proper name is just their dimension type, like overworld.
    # Worlds must be .init()ed, this loads their level.dat data and maybe other stuff later
    for ext, proper_name in zip(("", "_nether", "_the_end"), ("overworld", "nether", "the_end")):
        name = level_name + ext
        worlds[f'minecraft:{proper_name}'] = await World(server, name, os.path.join("worlds", name), region_cache_max_per).init()

    server.logger.info(f'Loaded default worlds: {", ".join([w.name for w in worlds.values()])}.')

    return worlds
