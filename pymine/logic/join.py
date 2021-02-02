import hashlib
import time
import uuid

from pymine.types.packet import Packet
from pymine.types.stream import Stream
import pymine.types.nbt as nbt

import pymine.net.packets.play.player as packets_player

from pymine.util.misc import seed_hash


async def join(server, stream: Stream, uuid_: uuid.UUID, username: str) -> None:
    level_name = server.conf["level_name"]

    player = server.playerio.fetch_player(uuid_)

    server.send_packet(
        stream,
        packets_player.PlayJoinGame(
            player.entity_id,
            server.conf["hardcore"],  # whether world is hardcore or not
            player.data['playerGameType'],  # gamemode
            player.data['previousPlayerGameType'],  # previous gamemode
            [level_name, f"{level_name}_nether", f"{level_name}_the_end"],  # world names
            nbt.TAG_Int(name="bruh", value=1),
            nbt.TAG_Int(name="bruh", value=1),
            player.data['Dimension'],  # Dimension/player the player is spawning in to
            seed_hash(server.conf["seed"]),
            server.conf["max_players"],
            server.conf["view_distance"],
            (not server.conf["debug"]),
            True,  # should be (not doImmediateRespawn gamerule)
            False,
            False,  # Should be true if world is superflat
        ),
    )
