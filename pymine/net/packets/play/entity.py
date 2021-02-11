"""Contains packets related to entities."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt

__all__ = (
    "PlayBlockEntityData",
    "PlayQueryEntityNBT",
    "PlayInteractEntity",
    "PlayEntityStatus",
    "PlayEntityAction",
    "PlayEntityPosition",
    "PlayEntityPositionAndRotation",
    "PlayEntityRotation",
    "PlayEntityMovement",
    "PlayRemoveEntityEffect",
    "PlayEntityHeadLook",
    "PlayAttachEntity",
    "PlayEntityVelocity",
    "PlayEntityTeleport",
    "PlayDestroyEntities",
    "PlayEntityMetadata",
    "PlayEntityEquipment",
)


class PlayBlockEntityData(Packet):
    """Sets the block entity associated with the block at the given location. (Server -> Client).

    :param int x: The x coordinate of the position.
    :param int y: The y coordinate of the position.
    :param int z: The z coordinate of the position.
    :param int action: The action to be carried out (see https://wiki.vg/Protocol#Block_Entity_Data).
    :param nbt.TAG nbt_data: The nbt data associated with the action/block.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar x:
    :ivar y:
    :ivar z:
    :ivar action:
    :ivar nbt_data:
    """

    id = 0x09
    to = 1

    def __init__(self, x: int, y: int, z: int, action: int, nbt_data: nbt.TAG) -> None:
        super().__init__()

        self.x, self.y, self.z = x, y, z
        self.action = action
        self.nbt_data = nbt_data

    def encode(self) -> bytes:
        return Buffer.pack_pos(self.x, self.y, self.z) + Buffer.pack("B", self.action) + Buffer.pack_nbt(self.nbt_data)


class PlayQueryEntityNBT(Packet):
    """Sent by the client when Shift+F3+I is used. (Client -> Server)

    :param int transaction_id: Incremental ID used so the client can verify responses.
    :param int entity_id: The ID of the entity to query.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar transaction_id:
    :ivar entity_id:
    """

    id = 0x0D
    to = 0

    def __init__(self, transaction_id: int, entity_id: int) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.entity_id = entity_id

    @classmethod
    def decode(cls, buf: Buffer) -> PlayQueryEntityNBT:
        return cls(buf.unpack_varint(), buf.unpack_varint())


class PlayInteractEntity(Packet):
    """Sent when a client clicks another entity, see here: https://wiki.vg/Protocol#Interact_Entity. (Client -> Server)

    :param int entity_id: The ID of the entity interacted with.
    :param int type_: Either interact (0), attack (1), or interact at (2).
    :param int target_x: The x coordinate of where the target is, can be None.
    :param int target_y: The y coordinate of where the target is, can be None.
    :param int target_z: The z coordinate of where the target is, can be None.
    :param int hand: The hand used.
    :param bool sneaking: Whether the client was sneaking or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar type_:
    :ivar target_x:
    :ivar target_y:
    :ivar target_z:
    :ivar hand:
    :ivar sneaking:
    """

    id = 0x0E
    to = 0

    def __init__(
        self, entity_id: int, type_: int, target_x: int, target_y: int, target_z: int, hand: int, sneaking: bool
    ) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.type_ = type_
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z
        self.hand = hand
        self.sneaking = sneaking

    @classmethod
    def decode(cls, buf: Buffer) -> PlayInteractEntity:
        return cls(
            buf.unpack_varint(),
            buf.unpack_varint(),
            buf.unpack_optional(buf.unpack_varint),
            buf.unpack_optional(buf.unpack_varint),
            buf.unpack_optional(buf.unpack_varint),
            buf.unpack_optional(buf.unpack_varint),
            buf.unpack("?"),
        )


class PlayEntityStatus(Packet):
    """Usually used to trigger an animation for an entity. (Server -> Client)


    :param int entity_id: The ID of the entity the status is for.
    :param int entity_status: Depends on the type of entity, see here: https://wiki.vg/Protocol#Entity_Status.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar entity_status:
    """

    id = 0x1A
    to = 1

    def __init__(self, entity_id: int, entity_status: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.entity_status = entity_status

    def encode(self) -> bytes:
        return Buffer.pack("i", self.entity_id) + Buffer.pack("b", self.entity_status)


class PlayEntityAction(Packet):
    """Sent by the client to indicate it has performed a certain action. (Client -> Server)

    :param int entity_id: The ID of the entity.
    :param int action_id: The action occurring, see here: https://wiki.vg/Protocol#Entity_Action.
    :param int jump_boost: Used with jumping while riding a horse.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar action_id:
    :ivar jump_boost:
    """

    id = 0x1C
    to = 0

    def __init__(self, entity_id: int, action_id: int, jump_boost: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.action_id = action_id
        self.jump_boost = jump_boost

    @classmethod
    def decode(cls, buf: Buffer) -> PlayEntityAction:
        return cls(buf.unpack_varint(), buf.unpack_varint(), buf.unpack_varint())


class PlayEntityPosition(Packet):
    """Sent by the server when an entity moves less than 8 blocks. (Server -> Client)

    :param int entity_id: The id of the entity moving.
    :param int dx: Delta (change in) x, -8 <-> 8.
    :param int dy: Delta (change in) y, -8 <-> 8.
    :param int dz: Delta (change in) z, -8 <-> 8.
    :param bool on_ground: Whether entity is on ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar dx:
    :ivar dy:
    :ivar dz:
    :ivar on_ground:
    """

    id = 0x27
    to = 1

    def __init__(self, entity_id: int, dx: int, dy: int, dz: int, on_ground: bool) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.dx, self.dy, self.dz = dx, dy, dz
        self.on_ground = on_ground

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack("h", self.dx)
            + Buffer.pack("h", self.dy)
            + Buffer.pack("h", self.dz)
            + Buffer.pack("?", self.on_ground)
        )


class PlayEntityPositionAndRotation(Packet):
    """Sent by the server when an entity rotates and moves. (Server -> Client)

    :param int entity_id: The id of the entity moving/rotationing.
    :param int dx: Delta (change in) x, -8 <-> 8.
    :param int dy: Delta (change in) y, -8 <-> 8.
    :param int dz: Delta (change in) z, -8 <-> 8.
    :param float yaw: The new yaw angle.
    :param float pitch: The new pitch angle.
    :param bool on_ground: Whether entity is on ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar dx:
    :ivar dy:
    :ivar dz:
    :ivar yaw:
    :ivar pitch:
    :ivar on_ground:
    """

    id = 0x28
    to = 1

    def __init__(self, entity_id: int, dx: int, dy: int, dz: int, yaw: float, pitch: float, on_ground: bool) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.dx, self.dy, self.dz = dx, dy, dz
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack("h", self.dx)
            + Buffer.pack("h", self.dy)
            + Buffer.pack("h", self.dz)
            + Buffer.pack("f", self.yaw)
            + Buffer.pack("f", self.pitch)
            + Buffer.pack("?", self.on_ground)
        )


class PlayEntityRotation(Packet):
    """Sent by the server when an entity rotates. (Server -> Client)

    :param float yaw: The new yaw angle.
    :param float pitch: The new pitch angle.
    :param bool on_ground: Whether entity is on ground or not.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar yaw:
    :ivar pitch:
    :ivar on_ground:
    """

    id = 0x29
    to = 1

    def __init__(self, entity_id: int, yaw: float, pitch: float, on_ground: bool) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack("f", self.yaw)
            + Buffer.pack("f", self.pitch)
            + Buffer.pack("?", self.on_ground)
        )


class PlayEntityMovement(Packet):
    """insert fancy doscstring here (server -> client)"""

    id = 0x2A
    to = 1

    def __init__(self, entity_id: int) -> None:
        super().__init__()

        self.entity_id = entity_id

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id)


class PlayRemoveEntityEffect(Packet):
    """insert fancy doscstring here (server -> client)"""

    id = 0x37
    to = 1

    def __init__(self, entity_id: int, effect_id: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.effect_id = effect_id

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack("b", self.effect_id)


class PlayEntityHeadLook(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x3A
    to = 1

    def __init__(self, entity_id: int, head_yaw: int) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.head_yaw = head_yaw

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack("B", self.head_yaw)


class PlayAttachEntity(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x45
    to = 1

    def __init__(self, attached_eid: int, holding_eid: int) -> None:
        super().__init__()

        self.attached_eid = attached_eid
        self.holding_eid = holding_eid

    def encode(self) -> bytes:
        return Buffer.pack("i", self.attached_eid) + Buffer.pack("i", self.holding_eid)


class PlayEntityVelocity(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x46
    to = 1

    def __init__(self, eid: int, velocity_x: int, velocity_y: int, velocity_z: int) -> None:
        super().__init__()

        self.eid = eid
        self.vel_x = velocity_x
        self.vel_y = velocity_y
        self.vel_z = velocity_z

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.eid)
            + Buffer.pack("h", self.vel_x)
            + Buffer.pack("h", self.vel_y)
            + Buffer.pack("h", self.vel_z)
        )


class PlayEntityTeleport(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x56
    to = 1

    def __init__(self, eid: int, x: int, y: int, z: int, yaw: int, pitch: int, on_ground: bool) -> None:
        super().__init__()

        self.eid = eid
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.on_ground = on_ground

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.eid)
            + Buffer.pack("d", self.x)
            + Buffer.pack("d", self.y)
            + Buffer.pack("d", self.z)
            + Buffer.pack("i", self.yaw)
            + Buffer.pack("i", self.pitch)
            + Buffer.pack("?", self.on_ground)
        )


class PlayDestroyEntities(Packet):
    """Insert fancy docstring here (server -> client)"""

    id = 0x36
    to = 1

    def __init__(self, entity_ids: list) -> None:
        super().__init__()

        self.entity_ids = entity_ids

    def encode(self) -> bytes:
        return Buffer.pack_varint(len(self.entity_ids)) + b"".join([Buffer.pack_varint(eid) for eid in self.entity_ids])


class PlayEntityMetadata(Packet):
    """Updates one or more metadata properties for an existing entity. (Server -> Client)

    :param int entity_id: The ID of the entity the data is for.
    :param dict metadata: The entity metadata, see here: https://wiki.vg/Protocol#Entity_Metadata.
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar metadata:
    """

    id = 0x44
    to = 1

    def __init__(self, entity_id: int, metadata: dict) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.metadata = metadata

    def encode(self) -> bytes:
        return Buffer.pack_varint(self.entity_id) + Buffer.pack_entity_metadata(self.metadata)


class PlayEntityEquipment(Packet):
    """Sends data about the entity's equipped equipment _

    :param int entity_id: The ID of the entity the equipment data is for.
    :param list equipment: An array of equipment,see here: <https://wiki.vg/Protocol>
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar entity_id:
    :ivar equipment:
    """

    id = 0x47
    to = 1

    def __init__(self, entity_id: int, equipment: list) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.equipment = equipment

    def encode(self) -> bytes:
        return (
            Buffer.pack_varint(self.entity_id)
            + Buffer.pack_varint(len(self.equipment))
            + b"".join([Buffer.pack("b", e[0]) + Buffer.pack_slot(**e[1]) for e in self.equipment])
        )


class PlayEntityProperties(Packet):
    """Sends information about certain attributes on an entity. (Server -> Client)"""

    id = 0x58
    to = 1

    def __init__(self, entity_id: int, properties: list) -> None:
        super().__init__()

        self.entity_id = entity_id
        self.properties = properties

    def encode(self) -> bytes:
        out = Buffer.pack_varint(self.entity_id)

        for prop in self.properties:
            out += (
                Buffer.pack_string(prop["key"])
                + Buffer.pack("d", prop["value"])
                + Buffer.pack_varint(len(prop["modifiers"]))
                + b"".join([Buffer.pack_modifier(m) for m in prop["modifiers"]])
            )
