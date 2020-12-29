"""Contains packets related to players."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = ('PlayAcknowledgePlayerDigging',)


class PlayAcknowledgePlayerDigging(Packet):
    """Sent by server to acknowledge player digging. (Server -> Client)

    :param int x: The x coordinate of where the player is digging.
    :param int y: The y coordinate of where the player is digging.
    :param int z: The z coordinate of where the player is digging.
    :param int block: The block state id of the block that is being broken/dug.
    :param int status: Value 0-2 to denote whether player should start, cancel, or finish.
    :param bool successful: True if the block was dug successfully.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr block:
    :attr status:
    :attr successful:
    """

    id_ = 0x07
    to = 1

    def __init__(self, x: int, y: int, z: int, block: int, status: int, successful: bool) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.z = z
        self.block = block
        self.status = status
        self.successful = successful

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + \
            Buffer.pack_varint(self.block) + \
            Buffer.pack_varint(self.status) + \
            Buffer.pack_bool(self.successful)


class PlayDisconnect(Packet):
    """Sent by the server before it disconnects a client. The client assumes that the server has already closed the connection by the time the packet arrives.

    Clientbound(Server -> Client)"""

    id_ = 0x19
    to = 1

    def __init__(self, reason: Chat):
        super().__init__()
        self.reason = reason

    def encode(self):
        return Buffer.pack_chat(self.reason)


class PlayPlayerAbilitiesClientBound(Packet):
    """Defines the player's abilities. (Server -> Client)

    :param bytes flags: Client data bitfield, see here: https://wiki.vg/Protocol#Player_Abilities_.28clientbound.29.
    :param float flying_speed: Speed at which client is flying.
    :param float fov_modifier: FOV modifier value.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr flags:
    :attr flying_speed:
    :attr fov_modifier:
    """

    id_ = 0x30
    to = 1

    def __init__(self, flags: bytes, flying_speed: float, fov_modifier: float) -> None:
        super().__init__()

        self.flags = flags
        self.flying_speed = flying_speed
        self.fov_modifier = fov_modifier

    def encode(self) -> bytes:
        return self.flags + Buffer.pack('f', self.flying_speed) + \
            Buffer.pack('f', self.fov_modifier)


class PlayPlayerAbilitiesServerBound(Packet):
    """Tells the server whether the client is flying or not. (Client -> Server)

    :param bool flying: Whether player is flying or not.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr flying:
    """

    id_ = 0x1A
    to = 0

    def __init__(self, flying: bool) -> None:
        super().__init__()

        self.flying = flying

    def decode(self, buf: Buffer) -> PlayPlayerAbilitiesServerBound:
        return (buf.unpack('b') == 0x02)


class PlayJoinGame(Packet):
    """Tells the client the necessary information to actually join the game. (Server -> Client)

    :param int entity_id: The player's entity ID.
    :param bool is_hardcore: Whether the world is hardcore mode or not.
    :param int gamemode: The player's gamemode.
    :param int prev_gamemode: The player's previous gamemode.
    :param list world_names: All of the worlds loaded on the server.
    :param 'nbt.Tag' dim_codec: Represents a dimension and biome registry, see here: https://wiki.vg/Protocol#Join_Game.
    :param 'nbt.Tag' dimension: A dimension type, see here: https://wiki.vg/Protocol#Join_Game.
    :param str world_name: The name of the world the player is joining.
    :param int hashed_seed: First 8 bytes of SHA-256 hash of the world's seed.
    :param int max_players: Max players allowed on the server, now ignored.
    :param int view_distance: Max view distance allowed by the server.
    :param bool reduced_debug_info: Whether debug info should be reduced or not.
    :param bool enable_respawn_screen: Set to false when the doImmediateRespawn gamerule is true.
    :param bool is_debug: If the world is a debug world.
    :param bool is_flat: If the world is a superflat world.
    :attr int id_: Unique packet ID.
    :attr int to: Packet direction.
    :attr entity_id:
    :attr is_hardcore:
    :attr gamemode:
    :attr prev_gamemode:
    :attr world_names:
    :attr dim_codec:
    :attr dimension:
    :attr world_name:
    :attr hashed_seed:
    :attr max_players:
    :attr view_distance:
    :attr reduced_debug_info:
    :attr enable_respawn_screen:
    :attr is_debug:
    :attr is_flat:
    """

    id_ = 0x24
    to = 1

    def __init__(self, entity_id: int, is_hardcore: bool, gamemode: int, prev_gamemode: int, world_names: list, dim_codec: 'nbt.Tag', dimension: 'nbt.Tag', world_name: str, hashed_seed: int, max_players: int, view_distance: int, reduced_debug_info: bool, enable_respawn_screen: bool, is_debug: bool, is_flat: bool):
        super().__init__()

        self.entity_id = entity_id
        self.is_hardcore = is_hardcore
        self.gamemode = gamemode
        self.prev_gamemode = prev_gamemode
        self.world_names = world_names
        self.dim_codec = dim_codec
        self.dimension = dimension
        self.world_name = world_name
        self.hashed_seed = hashed_seed
        self.max_players = max_players
        self.view_distance = view_distance
        self.reduced_debug_info = reduced_debug_info
        self.enable_respawn_screen = enable_respawn_screen
        self.is_debug = is_debug
        self.is_flat = is_flat

    def encode(self) -> bytes:
        return Buffer.pack('i', self.entity_id) + Buffer.pack_bool(self.is_hardcore) + \
            Buffer.pack('B', self.gamemode) + Buffer.pack('b', self.prev_gamemode) + \
            Buffer.pack_varint(len(self.world_names)) + \
            b''.join([Buffer.pack_string(w) for w in self.world_names]) + \
            Buffer.pack_nbt(self.dim_codec) + Buffer.pack_nbt(self.dimension) + \
            Buffer.pack_string(self.world_name) + Buffer.pack('q', self.hashed_seed) + \
            Buffer.pack_varint(self.max_players) + Buffer.pack_varint(self.view_distance) + \
            Buffer.pack_bool(self.reduced_debug_info) + \
            Buffer.pack_bool(self.enable_respawn_screen) + Buffer.pack_bool(self.is_debug) + \
            Buffer.pack_bool(self.is_flat)
