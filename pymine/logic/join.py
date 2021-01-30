import hashlib
import time

from pymine.types.packet import Packet
from pymine.types.stream import Stream
import pymine.types.nbt as nbt

import pymine.net.packets.play.player as packets_player

from pymine.util.misc import seed_hash
from pymine.server import server


async def join(stream: Stream, packet: Packet) -> None:
    lvl_name = server.conf["level_name"]

    # should be loaded from a cache on the disk or level.dat I think
    entity_id = server.cache.entity_id[stream.remote] = int(time.time())

    server.send_packet(
        stream,
        packets_player.PlayJoinGame(
            entity_id,
            server.conf["hardcore"],
            0,  # Should be current gamemode
            -1,  # Should be previous gamemode
            # Should be actual world names
            [f"minecraft:{lvl_name}", f"minecraft:{lvl_name}_nether", f"minecraft:{lvl_name}_the_end"],
            nbt.TAG_Int(name="bruh", value=1),
            nbt.TAG_Int(name="bruh", value=1),
            f"minecraft:{lvl_name}",  # should be actual current world name
            seed_hash(server.conf["seed"]),
            server.conf["max_players"],
            server.conf["view_distance"],
            (not server.conf["debug"]),
            True,  # should be (not doImmediateRespawn gamerule)
            False,
            False,  # Should be true if world is superflat
        ),
    )
