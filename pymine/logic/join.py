import hashlib
import time
import uuid

from pymine.types.packet import Packet
from pymine.types.stream import Stream
import pymine.types.nbt as nbt

from pymine.data.default_nbt.dimension_codec import new_dim_codec_nbt, get_dimension_data

import pymine.net.packets.play.player as packets_player
from pymine.util.misc import seed_hash


# Used to finish the process of allowing a client to actually enter the server
async def join(server, stream: Stream, uuid_: uuid.UUID, username: str) -> None:
    await send_join_game_packet(server, stream, uuid_)
    await send_server_brand(server, stream)


# crucial info pertaining to the world and player status
async def send_join_game_packet(server, stream: Stream, uuid_: uuid.UUID) -> None:
    level_name = server.conf["level_name"]  # level name, i.e. Xenon

    player = server.playerio.fetch_player(uuid_)
    world = server.worlds[player.data["Dimension"]]  # the world player *should* be spawning into

    await server.send_packet(
        stream,
        packets_player.PlayJoinGame(
            player.entity_id,
            server.conf["hardcore"],  # whether world is hardcore or not
            player.data["playerGameType"],  # gamemode
            player.data["previousPlayerGameType"],  # previous gamemode
            [level_name, f"{level_name}_nether", f"{level_name}_the_end"],  # world names
            new_dim_codec_nbt(),  # Shouldn't change unless CUSTOM DIMENSIONS are added fml
            # This is like the the dimension data for the dim the player is currently spawning into
            get_dimension_data(player.data["Dimension"]),  # player.data['Dimension'] should be like minecraft:overworld
            server.conf["level_name"],  # level name of the world the player is spawning into
            seed_hash(server.conf["seed"]),
            server.conf["max_players"],
            server.conf["view_distance"],
            (not server.conf["debug"]),
            (world.data["GameRules"]["doImmediateRespawn"] != "true"),  # (not doImmediateRespawn gamerule)
            False,  # If world is a debug world iirc
            False,  # Should be true if world is superflat
        ),
    )

# send server branch via plugin channels
async def send_server_brand(server, stream: Stream) -> None:
    pass
