"""Contains packets related to players."""

from __future__ import annotations
import uuid

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat
import pymine.types.nbt as nbt

__all__ = (
    "PlayPlayerDigging",
    "PlayAcknowledgePlayerDigging",
    "PlayDisconnect",
    "PlayPlayerAbilitiesClientBound",
    "PlayPlayerAbilitiesServerBound",
    "PlayJoinGame",
    "PlayPlayerPosition",
    "PlayPlayerPositionAndRotationServerBound",
    "PlayPlayerRotation",
    "PlayPlayerMovement",
    "PlayTeleportConfirm",
    "PlayClientStatus",
    "PlayClientSettings",
    "PlayCreativeInventoryAction",
    "PlaySpectate",
    "PlayCamera",
    "PlayUpdateViewPosition",
    "PlayUpdateViewDistance",
    "PlaySetExperience",
    "PlayUpdateHealth",
    "PlayCombatEvent",
    "PlayFacePlayer",
    "PlayPlayerInfo",
    "PlayRespawn",
)


class PlayPlayerDigging(Packet):
    """Sent by the client when the start mining a block. (Client -> Server)

    :param int status: The action the player is taking against the block, see here: https://wiki.vg/Protocol#Player_Digging.
    :param int x: The x coordinate of the block.
    :param int y: The y coordinate of the block.
    :param int z: The z coordinate of the block.
    :param int face: The face of the block that the player is mining.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar status:
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar face:
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
        return cls(buf.unpack_varint(), *buf.unpack_pos(), buf.unpack("b"))


class PlayAcknowledgePlayerDigging(Packet):
    """Sent by server to acknowledge player digging. (Server -> Client)

    :param int x: The x coordinate of where the player is digging.
    :param int y: The y coordinate of where the player is digging.
    :param int z: The z coordinate of where the player is digging.
    :param int block: The block state id of the block that is being broken/dug.
    :param int status: Value 0-2 to denote whether player should start, cancel, or finish.
    :param bool successful: True if the block was dug successfully.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar block:
    :ivar status:
    :ivar successful:
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
        return (
            Buffer.pack_pos(self.x, self.y, self.z)
            + Buffer.pack_varint(self.block)
            + Buffer.pack_varint(self.status)
            + Buffer.pack("?", self.successful)
        )


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
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar flags:
    :ivar flying_speed:
    :ivar fov_modifier:
    """

    id = 0x30
    to = 1

    def __init__(self, flags: int, flying_speed: float, fov_modifier: float) -> None:
        super().__init__()

        self.flags = flags
        self.flying_speed = flying_speed
        self.fov_modifier = fov_modifier

    def encode(self) -> bytes:
        return Buffer.pack("b", self.flags) + Buffer.pack("f", self.flying_speed) + Buffer.pack("f", self.fov_modifier)


class PlayPlayerAbilitiesServerBound(Packet):
    """Tells the server whether the client is flying or not. (Client -> Server)

    :param bool flying: Whether player is flying or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar flying:
    """

    id = 0x1A
    to = 0

    def __init__(self, flying: bool) -> None:
        super().__init__()

        self.flying = flying

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerAbilitiesServerBound:
        return cls(buf.unpack("b") == 0x02)


class PlayJoinGame(Packet):
    """Tells the client the necessary information to actually join the game. (Server -> Client)

    :param int entity_id: The player's entity ID.
    :param bool is_hardcore: Whether the world is hardcore mode or not.
    :param int gamemode: The player's gamemode.
    :param int prev_gamemode: The player's previous gamemode.
    :param list world_names: All of the worlds loaded on the server.
    :param nbt.TAG dim_codec: Represents a dimension and biome registry, see here: https://wiki.vg/Protocol#Join_Game.
    :param nbt.TAG dimension: A dimension type, see here: https://wiki.vg/Protocol#Join_Game.
    :param str world_name: The name of the world the player is joining.
    :param int hashed_seed: First 8 bytes of SHA-256 hash of the world's seed.
    :param int max_players: Max players allowed on the server, now ignored.
    :param int view_distance: Max view distance allowed by the server.
    :param bool reduced_debug_info: Whether debug info should be reduced or not.
    :param bool enable_respawn_screen: Set to false when the doImmediateRespawn gamerule is true.
    :param bool is_debug: If the world is a debug world.
    :param bool is_flat: If the world is a superflat world.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar is_hardcore:
    :ivar gamemode:
    :ivar prev_gamemode:
    :ivar world_names:
    :ivar dim_codec:
    :ivar dimension:
    :ivar world_name:
    :ivar hashed_seed:
    :ivar max_players:
    :ivar view_distance:
    :ivar reduced_debug_info:
    :ivar enable_respawn_screen:
    :ivar is_debug:
    :ivar is_flat:
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
        dim_codec: nbt.TAG,
        dimension: nbt.TAG,
        world_name: str,
        hashed_seed: int,
        max_players: int,
        view_distance: int,
        reduced_debug_info: bool,
        enable_respawn_screen: bool,
        is_debug: bool,
        is_flat: bool,
    ) -> None:
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
        return (
            Buffer.pack("i", self.entity_id)
            + Buffer.pack("?", self.is_hardcore)
            + Buffer.pack("B", self.gamemode)
            + Buffer.pack("b", self.prev_gamemode)
            + Buffer.pack_varint(len(self.world_names))
            + b"".join([Buffer.pack_string(w) for w in self.world_names])
            + Buffer.pack_nbt(self.dim_codec)
            + Buffer.pack_nbt(self.dimension)
            + Buffer.pack_string(self.world_name)
            + Buffer.pack("q", self.hashed_seed)
            + Buffer.pack_varint(self.max_players)
            + Buffer.pack_varint(self.view_distance)
            + Buffer.pack("?", self.reduced_debug_info)
            + Buffer.pack("?", self.enable_respawn_screen)
            + Buffer.pack("?", self.is_debug)
            + Buffer.pack("?", self.is_flat)
        )


class PlayPlayerPosition(Packet):
    """Used by the client to update the client's position. (Client -> Server)

    :param float x: The x coordinate of where the player is.
    :param float feet_y: The y coordinate of where the player's feet are.
    :param float z: The z coordinate of where the player is.
    :param bool on_ground: Whether the player/client is on the ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar feet_y:
    :ivar z:
    :ivar on_ground:
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
        return cls(buf.unpack("d"), buf.unpack("d"), buf.unpack("d"), buf.unpack("?"))


class PlayPlayerPositionAndRotationServerBound(Packet):
    """Packet sent by the client to update both position and rotation. (Client -> Server)

    :param float x: The x coordinate of where the player is.
    :param float feet_y: The y coordinate of where the player's feet are.
    :param float z: The z coordinate of where the player is.
    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :param bool on_ground: Whether the player/client is on the ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar feet_y:
    :ivar z:
    :ivar yaw:
    :ivar pitch:
    :ivar on_ground:
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
        return cls(buf.unpack("d"), buf.unpack("d"), buf.unpack("d"), buf.unpack("d"), buf.unpack("d"), buf.unpack("?"))


class PlayPlayerRotation(Packet):
    """Used by the client to update their rotation, see here: https://wiki.vg/Protocol#Player_Rotation. (Client -> Server)

    :param float yaw: The yaw (absolute rotation on x axis) in degrees.
    :param float pitch: The pitch (absolute rotation on y axis) in degrees.
    :param bool on_ground: Whether the player/client is on the ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar yaw:
    :ivar pitch:
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
        return cls(buf.unpack("d"), buf.unpack("d"), buf.unpack("?"))


class PlayPlayerMovement(Packet):
    """Tells server whether client/player is on ground or not. (Client -> Server)

    :param bool on_ground: Whether the player/client is on the ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar on_ground:
    """

    id = 0x15
    to = 0

    def __init__(self, on_ground: bool) -> None:
        super().__init__()

        self.on_ground = on_ground

    @classmethod
    def decode(cls, buf: Buffer) -> PlayPlayerMovement:
        return cls(buf.unpack("?"))


class PlayTeleportConfirm(Packet):
    """Sent by the client as a confirmation to a player position and look packet. (Client -> Server)

    :param int teleport_id: ID given by a player pos and look packet.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar teleport_id:
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
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar action_id:
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
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar locale:
    :ivar view_distance:
    :ivar chat_mode:
    :ivar chat_colors:
    :ivar displayed_skin_parts:
    :ivar main_hand:
    """

    id = 0x05
    to = 0

    def __init__(
        self, locale: str, view_distance: int, chat_mode: int, chat_colors: bool, displayed_skin_parts: int, main_hand: int
    ) -> None:
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
            buf.unpack_string(), buf.unpack("b"), buf.unpack_varint(), buf.unpack("?"), buf.unpack("B"), buf.unpack_varint()
        )


class PlayCreativeInventoryAction(Packet):
    """Sent when a client/player clicks in their inventory in creative mode. (Client -> Server)

    :param int slot: The inventory slot that was clicked.
    :param dict clicked_item: The actual slot data for the clicked item.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar slot:
    :ivar clicked_item:
    """

    id = 0x28
    to = 0

    def __init__(self, slot: int, clicked_item: dict) -> None:
        super().__init__()

        self.slot = slot
        self.clicked_item = clicked_item

    @classmethod
    def decode(cls, buf: Buffer) -> PlayCreativeInventoryAction:
        return cls(buf.unpack("h"), buf.unpack_slot())


class PlaySpectate(Packet):
    """Used by the client to spectate a given entity. (Client -> Server)

    :param uuid.UUID target: The target entity/player to teleport to and spectate.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar target:
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
        return Buffer.pack("f", self.xp_bar) + Buffer.pack_varint(self.lvl) + Buffer.pack_varint(self.total_xp)


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
        return Buffer.pack("f", self.health) + Buffer.pack_varint(self.food) + Buffer.pack("f", self.saturation)


class PlayCombatEvent(Packet):
    """Sent by the server to display the game over screen. (Server -> Client)

    :param int event: The event that occurred, either enter combat (0), end combat (1), or entity dead (2).
    :param dict data: Depends on what event occurred.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar event:
    :ivar data:
    """

    id = 0x31
    to = 1

    def __init__(self, event: int, data: dict = None) -> None:
        super().__init__()

        self.event = event
        self.data = data

    def encode(self) -> bytes:
        # if self.event == 0:  # start combat
        #     return Buffer.pack_varint(self.event)
        #
        # if self.event == 1:  # end combat
        #     return Buffer.pack_varint(self.event) + Buffer.pack_varint(self.data['duration']) + \
        #         Buffer.pack('i', self.data['opponent'])

        if self.event == 2:  # entity dead, only one actually used
            return (
                Buffer.pack_varint(self.event)
                + Buffer.pack_varint(self.data["player_id"])
                + Buffer.pack("i", self.data["entity_id"])
                + Buffer.pack_chat(self.data["message"])
            )


class PlayPlayerInfo(Packet):
    """Sent by the server to update the user list under the tab menu. (Server -> Client)

    :param int action: The action to be taken, either add player (0), update gamemode (1), update latency (2), update display name (3), or remove player (4).
    :param list players: A list of dictionaries, content varies depending on action, see here: https://wiki.vg/Protocol#Player_Info.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar action:
    :ivar players:
    """

    id = 0x32
    to = 1

    def __init__(self, action: int, players: list) -> None:
        super().__init__()

        self.action = action
        self.players = players

    def encode(self) -> bytes:
        out = Buffer.pack_varint(self.action) + len(self.players)

        if self.action == 0:  # add player
            for player in self.players:
                out += (
                    Buffer.pack_uuid(player["uuid"])
                    + Buffer.pack_string(player["name"])
                    + Buffer.pack_varint(len(player["properties"]))
                )

                for prop in player["properties"]:
                    out += (
                        Buffer.pack_string(prop["name"])
                        + Buffer.pack_string(prop["value"])
                        + Buffer.pack_optional(Buffer.pack_string, prop.get("signature"))
                    )

                out += (
                    Buffer.pack_varint(player["gamemode"])
                    + Buffer.pack_varint(player["ping"])
                    + Buffer.pack_optional(Buffer.pack_chat, player["display_name"])
                )
        elif self.action == 1:  # update gamemode
            out += b"".join([Buffer.pack_uuid(p["uuid"]) + Buffer.pack_varint(p["gamemode"]) for p in self.players])
        elif self.action == 2:  # update latency
            out += b"".join([Buffer.pack_uuid(p["uuid"]) + Buffer.pack_varint(p["ping"]) for p in self.players])
        elif self.action == 3:  # update display name
            out += b"".join([Buffer.pack_uuid(p["uuid"]) + Buffer.pack_optional(p.get("display_name")) for p in self.players])
        elif self.action == 4:
            out += b"".join([Buffer.pack_uuid(p["uuid"]) for p in self.players])

        return out


class PlayFacePlayer(Packet):
    """Used by the server to rotate the client player to face the given location or entity. (Server -> Client)

    :param int feet_or_eyes: Whether to aim using the head position (1) or feet (0)
    :param float tx: The x coordinate of the point to face towards.
    :param float ty: The y coordinate of the point to face towards.
    :param float tz: The z coordinate of the point to face towards.
    :param bool is_entity: If true, additional info is provided.
    :param int entity_id: The entity ID.
    :param int entity_feet_or_eyes: Same as regular feet_or_eyes.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar feet_or_eyes:
    :ivar tx:
    :ivar ty:
    :ivar tz:
    :ivar entity_id:
    :ivar entity_feet_or_eyes:
    """

    id = 0x33
    to = 1

    def __init__(
        self,
        feet_or_eyes: int,
        tx: float,
        ty: float,
        tz: float,
        is_entity: bool,
        entity_id: int = None,
        entity_feet_or_eyes: int = None,
    ) -> None:
        super().__init__()

        self.feet_or_eyes = feet_or_eyes
        self.tx, self.ty, self.tz = tx, ty, tz
        self.is_entity = is_entity
        self.entity_id = entity_id
        self.entity_feet_or_eyes = entity_feet_or_eyes

    def encode(self) -> bytes:
        out = (
            Buffer.pack_varint(self.feet_or_eyes)
            + Buffer.pack("d", self.tx)
            + Buffer.pack("d", self.ty)
            + Buffer.pack("d", self.tz)
        )

        if self.is_entity:
            out += Buffer.pack_varint(self.entity_id) + Buffer.pack_varint(self.entity_feet_or_eyes)

        return out


class PlayRespawn(Packet):
    """Sent to change a player's dimension. (Server -> Client)

    :param nbt.TAG dimension: A dimension defined via the dimension registry.
    :param str world_name: Name of the world the player entity is being spawned into.
    :param int hashed_seed: First 8 bytes of the sha-256 hash of the seed.
    :param int gamemode: The current gamemode of the player entity.
    :param int prev_gamemode: The previous gamemode of the player entity.
    :param bool is_debug: True if the world is a debug world.
    :param bool is_flat: Whether the new world/dimension is a superflat one or not.
    :param bool copy_metadata: If false, metadata is reset on the spawned player entity. Should be True for dimension changes.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar dimension:
    :ivar world_name:
    :ivar hashed_seed:
    :ivar gamemode:
    :ivar prev_gamemode:
    :ivar is_debug:
    :ivar is_flat:
    :ivar copy_metadata:
    """

    id = 0x39
    to = 1

    def __init__(
        self,
        dimension: nbt.TAG,
        world_name: str,
        hashed_seed: int,
        gamemode: int,
        prev_gamemode: int,
        is_debug: bool,
        is_flat: bool,
        copy_metadata: bool,
    ) -> None:
        super().__init__()

        self.dimension = dimension
        self.world_name = world_name
        self.hashed_seed = hashed_seed
        self.gamemode = gamemode
        self.prev_gamemode = prev_gamemode
        self.is_debug = is_debug
        self.is_flat = is_flat
        self.copy_metadata = copy_metadata

    def encode(self) -> bytes:
        return (
            Buffer.pack_nbt(self.dimension)
            + Buffer.pack_string(self.world_name)
            + Buffer.pack("l", self.hashed_seed)
            + Buffer.pack("B", self.gamemode)
            + Buffer.pack("B", self.prev_gamemode)
            + Buffer.pack("?", self.is_debug)
            + Buffer.pack("?", self.is_flat)
            + Buffer.pack("?", self.copy_metadata)
        )
