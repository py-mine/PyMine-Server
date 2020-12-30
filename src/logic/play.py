import hashlib
import time

from src.types.packets.play import player as packets_player
from src.types.buffer import Buffer

from src.util.share import share, logger, entity_id_cache, user_cache
from src.util.seeds import seed_hash


async def play(r: 'StreamReader', w: 'StreamWriter', packet: 'Packet', remote: tuple) -> tuple:
    pass


async def finish_login(r: 'StreamReader', w: 'StreamWriter', remote: tuple) -> None:
    lvl_name = share['conf']['level_name']
    entity_id = entity_id_cache.get(remote)

    if entity_id is None:
        entity_id_cache[remote] = int(time.time())

    w.write(Buffer.pack_packet(packets_player.PlayJoinGame(
        entity_id,
        share['conf']['hardcore'],
        0,  # Shoudl be current gamemode
        -1,  # Should be previous gamemode
        [f'minecraft:{lvl_name}', f'minecraft:{lvl_name}_nether', f'minecraft:{lvl_name}_the_end'],  # Should be actual world names
        dim_codec,
        dimension,
        f'minecraft:{lvl_name}',  # should be actual current world name
        seed_hash(share['conf']['seed']),
        share['conf']['max_players'],
        share['conf']['view_distance'],
        (not share['conf']['debug']),
        True,  # should be (not doImmediateRespawn gamerule)
        False,
        False  # Should be true if world is superflat
    )))

    await w.drain()
