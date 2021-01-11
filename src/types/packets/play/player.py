"""Contains packets related to players."""

from __future__ import annotations
from nbt import nbt
import uuid

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

__all__ = (
    'PlayPlayerDigging',
    'PlayAcknowledgePlayerDigging',
    'PlayDisconnect',
    'PlayPlayerAbilitiesClientBound',
    'PlayPlayerAbilitiesServerBound',
    'PlayJoinGame',
    'PlayPlayerPosition',
    'PlayPlayerPositionAndRotationServerBound',
    'PlayPlayerRotation',
    'PlayPlayerMovement',
    'PlayTeleportConfirm',
    'PlayClientStatus',
    'PlayClientSettings',
    'PlayCreativeInventoryAction',
    'PlaySpectate',
    'PlayCamera',
    'PlayUpdateViewPosition',
    'PlayUpdateViewDistance',
    'PlaySetExperience',
    'PlayUpdateHealth',
)


class PlayPlayerDigging(Packet):
    """Sent by the client when the start mining a block. (Client -> Server)

    :param int status: The action the player is taking against the block, see here: https://wiki.vg/Protocol#Player_Digging.
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :param int face: The face of the block that the player is mining.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr status:
    :attr x:
    :attr y:
    :attr z:
    :attr face:
    """

    id = 0x1B
    to = 0

    def __init__(self, status: int, x: int, y: int, z: int, face: int) -> None:
        super().__init__()

        self.status = status
        self.x, self.y, self.z = x, y, z
        self.face = face

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerDigging:
        return cls(buf.unpack_varint(), *buf.unpack_pos(), buf.unpack('b'))


class PlayAcknowledgePlayerDigging(Packet):
    """Sent by server to acknowledge player digging. (Server -> Client)

    :param int x: The x coordinate of where the player is digging.
    :param int y: The y coordinate of where the player is digging.
    :param int z: The z coordinate of where the player is digging.
    :param int block: The block state id of the block that is being broken/dug.
    :param int status: Value 0-2 to denote whether player should start, cancel, or finish.
    :param bool successful: True if the block was dug successfully.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr y:
    :attr z:
    :attr block:
    :attr status:
    :attr successful:
    """

    id = 0x07
    to = 1

    def __init__(self, x: int, y: int, z: int, block: int, status: int, successful: bool) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.block = block
        self.status = status
        self.successful = successful

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + Buffer.pack_varint(self.block) + Buffer.pack_varint(self.status) + \
            Buffer.pack('?', self.successful)


class PlayDisconnect(Packet):
    """Sent by the server before it disconnects a client. The client assumes that the server has already closed the connection by the time the packet arrives.

    Clientbound(Server -> Client)"""

    id = 0x19
    to = 1

    def __init__(self, reason: Chat) -> None:
        super().__init__()

        self.reason = reason

    def encode(self) -> bytes:
        return Buffer.pack_chat(self.reason)


class PlayPlayerAbilitiesClientBound(Packet):
    """Defines the player's abilities. (Server -> Client)

    :param bytes flags: Client data bitfield, see here: https://wiki.vg/Protocol#Player_Abilities_.28clientbound.29.
    :param float flying_speed: Speed at which client is flying.
    :param float fov_modifier: FOV modifier value.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr flags:
    :attr flying_speed:
    :attr fov_modifier:
    """

    id = 0x30
    to = 1

    def __init__(self, flags: bytes, flying_speed: float, fov_modifier: float) -> None:
        super().__init__()

        self.flags = flags
        self.flying_speed = flying_speed
        self.fov_modifier = fov_modifier

    def encode(self) -> bytes:
        return self.flags + Buffer.pack('f', self.flying_speed) + Buffer.pack('f', self.fov_modifier)


class PlayPlayerAbilitiesServerBound(Packet):
    """Tells the server whether the client is flying or not. (Client -> Server)

    :param bool flying: Whether player is flying or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr flying:
    """

    id = 0x1A
    to = 0

    def __init__(self, flying: bool) -> None:
        super().__init__()

        self.flying = flying

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerAbilitiesServerBound:
        return cls(buf.unpack('b') == 0x02)


class PlayJoinGame(Packet):
    """Tells the client the necessary information to actually join the game. (Server -> Client)

    :param int entity_id: The player's entity ID.
    :param bool is_hardcore: Whether the world is hardcore mode or not.
    :param int gamemode: The player's gamemode.
    :param int prev_gamemode: The player's previous gamemode.
    :param list world_names: All of the worlds loaded on the server.
    :param nbt.Tag dim_codec: Represents a dimension and biome registry, see here: https://wiki.vg/Protocol#Join_Game.
    :param nbt.Tag dimension: A dimension type, see here: https://wiki.vg/Protocol#Join_Game.
    :param str world_name: The name of the world the player is joining.
    :param int hashed_seed: First 8 bytes of SHA-256 hash of the world's seed.
    :param int max_players: Max players allowed on the server, now ignored.
    :param int view_distance: Max view distance allowed by the server.
    :param bool reduced_debug_info: Whether debug info should be reduced or not.
    :param bool enable_respawn_screen: Set to false when the doImmediateRespawn gamerule is true.
    :param bool is_debug: If the world is a debug world.
    :param bool is_flat: If the world is a superflat world.
    :attr int id: Unique packet ID.
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

    id = 0x24
    to = 1

    def __init__(
            self,
            entity_id: int,
            is_hardcore: bool,
            gamemode: int,
            prev_gamemode: int,
            world_names: list,
            dim_codec: nbt.Tag,
            dimension: nbt.Tag,
            world_name: str,
            hashed_seed: int,
            max_players: int,
            view_distance: int,
            reduced_debug_info: bool,
            enable_respawn_screen: bool,
            is_debug: bool,
            is_flat: bool) -> None:
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
        return Buffer.pack('i', self.entity_id) + Buffer.pack('?', self.is_hardcore) + \
            Buffer.pack('B', self.gamemode) + Buffer.pack('b', self.prev_gamemode) + \
            Buffer.pack_varint(len(self.world_names)) + \
            b''.join(Buffer.pack_string(w) for w in self.world_names) + \
            Buffer.pack_nbt(self.dim_codec) + Buffer.pack_nbt(self.dimension) + \
            Buffer.pack_string(self.world_name) + Buffer.pack('q', self.hashed_seed) + \
            Buffer.pack_varint(self.max_players) + Buffer.pack_varint(self.view_distance) + \
            Buffer.pack('?', self.reduced_debug_info) + Buffer.pack('?', self.enable_respawn_screen) + \
            Buffer.pack('?', self.is_debug) + Buffer.pack('?', self.is_flat)


class PlayPlayerPosition(Packet):
    """Used by the client to update the client's position. (Client -> Server)

    :param float x: The x coordinate of where the player is.
    :param float feet_y: The y coordinate of where the player's feet are.
    :param float z: The z coordinate of where the player is.
    :param bool on_ground: Whether the player/client is on the ground or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr feet_y:
    :attr z:
    :attr on_ground:
    """

    id = 0x12
    to = 0

    def __init__(self, x: float, feet_y: float, z: float, on_ground: bool) -> None:
        super().__init__()

        self.x = x
        self.feet_y = feet_y
        self.z = z
        self.on_ground = on_ground

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerPosition:
        return cls(buf.unpack('d'), buf.unpack('d'), buf.unpack('d'), buf.unpack('?'))


class PlayPlayerPositionAndRotationServerBound(Packet):
    """Packet sent by the client to update both position and rotation. (Client -> Server)

    :param float x: The x coordinate of where the player is.
    :param float feet_y: The y coordinate of where the player's feet are.
    :param float z: The z coordinate of where the player is.
    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :param bool on_ground: Whether the player/client is on the ground or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr x:
    :attr feet_y:
    :attr z:
    :attr yaw:
    :attr pitch:
    :attr on_ground:
    """

    id = 0x13
    to = 0

    def __init__(self, x: float, feet_y: float, z: float, yaw: float, pitch: float, on_ground: bool) -> None:
        super().__init__()

        self.x = x
        self.feet_y = feet_y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerPositionAndRotationServerBound:
        return cls(
            buf.unpack('d'),
            buf.unpack('d'),
            buf.unpack('d'),
            buf.unpack('d'),
            buf.unpack('d'),
            buf.unpack('?')
        )


class PlayPlayerRotation(Packet):
    """Used by the client to update their rotation, see here: https://wiki.vg/Protocol#Player_Rotation. (Client -> Server)

    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :param bool on_ground: Whether the player/client is on the ground or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr yaw:
    :attr pitch:
    """

    id = 0x14
    to = 0

    def __init__(self, yaw: float, pitch: float, on_ground: bool) -> None:
        super().__init__()

        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerRotation:
        return cls(buf.unpack('d'), buf.unpack('d'), buf.unpack('?'))


class PlayPlayerMovement(Packet):
    """Tells server whether client/player is on ground or not. (Client -> Server)

    :param bool on_ground: Whether the player/client is on the ground or not.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr on_ground:
    """

    id = 0x15
    to = 0

    def __init__(self, on_ground: bool) -> None:
        super().__init__()

        self.on_ground = on_ground

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerMovement:
        return cls(buf.unpack('?'))


class PlayTeleportConfirm(Packet):
    """Sent by the client as a confirmation to a player position and look packet. (Client -> Server)

    :param int teleport_id: ID given by a player pos and look packet.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr teleport_id:
    """

    id = 0x00
    to = 0

    def __init__(self, teleport_id: int) -> None:
        super().__init__()

        self.teleport_id = teleport_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayTeleportConfirm:
        return cls(buf.unpack_varint())


class PlayClientStatus(Packet):
    """Used by the client to denote when the client has either (0) clicked respawn button or (1) opened the statistics menu. (Client -> Server)

    :param int action_id: Whether client has (0) clicked respawn or (1) opened stats menu.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr action_id:
    """

    id = 0x04
    to = 0

    def __init__(self, action_id: int) -> None:
        super().__init__()

        self.action_id = action_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayClientStatus:
        return cls(buf.unpack_varint())


class PlayClientSettings(Packet):
    """Used by client to update its settings either on server join or whenever. (Client -> Server)

    :param str locale: The locale of the client, example: en_US or en_GB.
    :param int view_distance: The client's view distance.
    :param int chat_mode: The client's chat mode, see here: https://wiki.vg/Protocol#Keep_Alive_.28clientbound.29.
    :param bool chat_colors: Whether the client has chat colors enabled or not.
    :param int displayed_skin_parts: A bit mask describing which parts of the client's skin are visible.
    :param int main_hand: Either left (0) or right (1).
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr locale:
    :attr view_distance:
    :attr chat_mode:
    :attr chat_colors:
    :attr displayed_skin_parts:
    :attr main_hand:
    """

    id = 0x05
    to = 0

    def __init__(
            self,
            locale: str,
            view_distance: int,
            chat_mode: int,
            chat_colors: bool,
            displayed_skin_parts: int,
            main_hand: int) -> None:
        super().__init__()

        self.locale = locale
        self.view_distance = view_distance
        self.chat_mode = chat_mode
        self.chat_colors = chat_colors
        self.displayed_skin_parts = displayed_skin_parts
        self.main_hand = main_hand

    @classmethod
    def decode(cls, buf: Buffer) -> PlayClientSettings:
        return cls(
            buf.unpack_string(),
            buf.unpack('b'),
            buf.unpack_varint(),
            buf.unpack('?'),
            buf.unpack('B'),
            buf.unpack_varint()
        )


class PlayCreativeInventoryAction(Packet):
    """Sent when a client/player clicks in their inventory in creative mode. (Client -> Server)

    :param int slot: The inventory slot that was clicked.
    :param dict clicked_item: The actual slot data for the clicked item.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr slot:
    :attr clicked_item:
    """

    id = 0x28
    to = 0

    def __init__(self, slot: int, clicked_item: dict) -> None:
        super().__init__()

        self.slot = slot
        self.clicked_item = clicked_item

    @classmethod
    def decode(cls, buf: Buffer) -> PlayCreativeInventoryAction:
        return cls(buf.unpack('h'), buf.unpack_slot())


class PlaySpectate(Packet):
    """Used by the client to spectate a given entity. (Client -> Server)

    :param uuid.UUID target: The target entity/player to teleport to and spectate.
    :attr int id: Unique packet ID.
    :attr int to: Packet direction.
    :attr target:
    """

    id = 0x2D
    to = 0

    def __init__(self, target: uuid.UUID) -> None:
        super().__init__()

        self.target = target

    @classmethod
    def decode(cls, buf: Buffer) -> PlaySpectate:
        return cls(buf.unpack_uuid())


class PlayCamera(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x3E
    to = 1

    def __init__(self, camera_id: int) -> None:
        super().__init__()

        self.camera_id = camera_id

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.camera_id)


class PlayUpdateViewPosition(Packet):
    """insert fancy docstring here (server -> client)"""

    id = 0x40
    to = 1

    def __init__(self, chunk_x: int, chunk_z: int) -> None:
        super().__init__()

        self.chunk_x = chunk_x
        self.chunk_z = chunk_z

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.chunk_x) + Buffer.pack_varint(self.chunk_z)


class PlayUpdateViewDistance(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x41
    to = 1

    def __init__(self, view_distance: int) -> None:
        super().__init__()

        self.view_distance = view_distance

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.view_distance)


class PlaySetExperience(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x48
    to = 1

    def __init__(self, xp_bar: float, lvl: int, total_xp: int) -> None:
        super().__init__()

        self.xp_bar = xp_bar
        self.lvl = lvl
        self.total_xp = total_xp

    def encode(self) -> bytes:
        return Buffer.pack('f', self.xp_bar) + Buffer.pack_varint(self.lvl) + Buffer.pack_varint(self.total_xp)


class PlayUpdateHealth(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x49
    to = 1

    def __init__(self, health: float, food: int, saturation: float) -> None:
        super().__init__()

        self.health = health
        self.food = food
        self.saturation = saturation

    def encode(self) -> bytes:
        return Buffer.pack('f', self.health) + Buffer.pack_varint(self.food) + Buffer.pack('f', self.saturation)
