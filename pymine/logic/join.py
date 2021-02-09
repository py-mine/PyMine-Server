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
from pymine.data.recipes import RECIPES
from pymine.data.tags import TAGS

import pymine.net.packets.play as play_packets
from pymine.util.misc import seed_hash
from pymine.server import server


# Used to finish the process of allowing a client to actually enter the server
async def join(stream: Stream, uuid_: uuid.UUID, username: str) -> None:
    server.cache.uuid[stream.remote] = int(uuid_)  # update uuid cache

    player = await server.playerio.fetch_player(uuid_)  # fetch player data from disk
    player.remote = stream.remote
    player.username = username

    world = server.worlds[player.data["Dimension"].data]  # the world player *should* be spawning into

    await send_join_game_packet(stream, world, player)

    # send server brand via plugin channels
    await server.send_packet(
        stream, play_packets.plugin_msg.PlayPluginMessageClientBound("minecraft:brand", Buffer.pack_string(server.meta.pymine))
    )

    # sends info about the server difficulty
    await server.send_packet(
        stream,
        play_packets.difficulty.PlayServerDifficulty(world.data["Difficulty"].data, world.data["DifficultyLocked"].data),
    )

    await send_player_abilities(stream, player)


async def join_2(stream: Stream, player: Player) -> None:
    # change held item to saved last held item
    await server.send_packet(stream, play_packets.player.PlayHeldItemChangeClientBound(player.data["SelectedItemSlot"].data))

    # send recipes
    await server.send_packet(stream, play_packets.crafting.PlayDeclareRecipes(RECIPES))

    # send tags (data about the different blocks and items)
    await server.send_packet(stream, play_packets.tags.PlayTags(TAGS))

    # send entity status packet, apparently this is required, for now it'll just set player to op lvl 4 (value 28)
    await server.send_packet(stream, play_packets.entity.PlayEntityStatus(player.entity_id, 28))


# crucial info pertaining to the world and player status
async def send_join_game_packet(stream: Stream, world: World, player: Player) -> None:
    level_name = server.conf["level_name"]  # level name, i.e. Xenon

    await server.send_packet(
        stream,
        play_packets.player.PlayJoinGame(
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
        play_packets.player.PlayPlayerAbilitiesClientBound(
            flags.field, abilities["flySpeed"].data, abilities["walkSpeed"].data
        ),
    )
