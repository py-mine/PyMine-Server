import hashlib
import time
import uuid

from pymine.types.bitfield import BitField
from pymine.types.buffer import Buffer
from pymine.types.packet import Packet
from pymine.types.player import Player
from pymine.types.stream import Stream
from pymine.types.world import World
import pymine.types.nbt as nbt

from pymine.data.default_nbt.dimension_codec import new_dim_codec_nbt, get_dimension_data

import pymine.net.packets.play.difficulty as packets_difficulty
import pymine.net.packets.play.plugin_msg as packets_plugin
import pymine.net.packets.play.player as packets_player

from pymine.util.misc import seed_hash
from pymine.server import server


# Used to finish the process of allowing a client to actually enter the server
async def join(stream: Stream, uuid_: uuid.UUID, username: str) -> None:
    server.cache.uuid[stream.remote] = int(uuid_)  # update uuid cache

    player = await server.playerio.fetch_player(uuid_)  # fetch player data from disk
    player.set_meta(username, stream.remote)

    world = server.worlds[player.data["Dimension"].data]  # the world player *should* be spawning into

    await send_join_game_packet(stream, world, player)
    await send_server_brand(stream)
    await send_server_difficulty(stream, world)
    await send_player_abilities(stream, player)


@server.api.events.on_packet("play", 0x0B)
async def plugin_message_recv(stream: Stream, packet: Packet):
    if packet.channel == "minecraft:brand":
        server.cache.uuid[stream.remote].brand = packet.data.unpack_string()


# crucial info pertaining to the world and player status
async def send_join_game_packet(stream: Stream, world: World, player: Player) -> None:
    level_name = server.conf["level_name"]  # level name, i.e. Xenon

    await server.send_packet(
        stream,
        packets_player.PlayJoinGame(
            player.entity_id,
            server.conf["hardcore"],  # whether world is hardcore or not
            player.data["playerGameType"].data,  # gamemode
            player.data["previousPlayerGameType"].data,  # previous gamemode
            [level_name, f"{level_name}_nether", f"{level_name}_the_end"],  # world names
            new_dim_codec_nbt(),  # Shouldn't change unless CUSTOM DIMENSIONS are added fml
            # This is like the the dimension data for the dim the player is currently spawning into
            get_dimension_data(player.data["Dimension"].data),  # player.data['Dimension'] should be like minecraft:overworld
            server.conf["level_name"],  # level name of the world the player is spawning into
            seed_hash(server.conf["seed"]),
            server.conf["max_players"],
            server.conf["view_distance"],
            (not server.conf["debug"]),
            (world.data["GameRules"]["doImmediateRespawn"].data != "true"),  # (not doImmediateRespawn gamerule)
            False,  # If world is a debug world iirc
            False,  # Should be true if world is superflat
        ),
    )


# send server brand + version via plugin channels
async def send_server_brand(stream: Stream) -> None:
    await server.send_packet(
        stream, packets_plugin.PlayPluginMessageClientBound("minecraft:brand", Buffer.pack_string(server.meta.pymine))
    )


# shown in the menu options for the client
async def send_server_difficulty(stream: Stream, world: World) -> None:
    await server.send_packet(
        stream, packets_difficulty.PlayServerDifficulty(world.data["Difficulty"].data, world.data["DifficultyLocked"].data)
    )


# send what the player can/can't do
async def send_player_abilities(stream: Stream, player: Player) -> None:
    abilities = player.data["abilities"]
    flags = BitField.new(4)

    flags.add(0x01, abilities["invulnerable"].data)
    flags.add(0x02, abilities["flying"].data)
    flags.add(0x04, abilities["mayfly"].data)
    flags.add(0x08, abilities["instabuild"].data)

    await server.send_packet(  # yes the last arg is supposed to be fov, but the values are actually the same
        stream,
        packets_player.PlayPlayerAbilitiesClientBound(flags.field, abilities["flySpeed"].data, abilities["walkSpeed"].data),
    )
