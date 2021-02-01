from __future__ import annotations

import uuid

import pymine.types.nbt as nbt


class Player:
    def __init__(self, entity_id: int, data: nbt.TAG) -> None:
        self.entity_id = entity_id
        self.data = data

        self.uuid = uuid.UUID(bytes=struct.pack(">iiii", *data["uuid"]))
        self.x, self.y, self.z = self.pos = data["Pos"]

        self.username = None
        self.remote = None

    def set_meta(self, username: str, remote: tuple) -> None:
        self.username = username
        self.remote = remote

    def new_nbt_data(self, uuid_: uuid.UUID) -> nbt.TAG:
        return nbt.TAG_Compound(
            "",
            [
                nbt.TAG_String("id", "minecraft:player"),
                nbt.TAG_List("Pos", [nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0)]),
                nbt.TAG_List("Motion", [nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0), nbt.TAG_Double(None, 0)]),
                nbt.TAG_List("Rotation", [nbt.TAG_Float(None, 0), nbt.TAG_Float(None, 0)]),
                nbt.TAG_Float("FallDistance", 0),
                nbt.TAG_Short("Fire", -20),
                nbt.TAG_Short("Air", 300),
                nbt.TAG_Byte("OnGround", 1),
                nbt.TAG_Byte("NoGravity", 0),
                nbt.TAG_Byte("Invulnerable", 0),
                nbt.TAG_Int("PortalCooldown", 0),
                nbt.TAG_Int_Array("UUID", struct.unpack(">iiii", uuid_.bytes)),
                nbt.TAG_String("CustomName", ""),
                nbt.TAG_Byte("CustomNameVisible", 0),
                nbt.TAG_Byte("Silent", 0),
                nbt.TAG_List("Passengers", []),
                nbt.TAG_Byte("Glowing", 0),
                nbt.TAG_List("Tags", []),
                nbt.TAG_Float("Health", 20),
                NBT.TAG_Float("AbsorptionAmount", 0),
                nbt.TAG_Short("HurtTime", 0),
                nbt.TAG_Int("HurtByTimestamp", 0),
                nbt.TAG_Short("DeathTime", 0),
                nbt.TAG_Byte("FallFlying", 0),
                # nbt.TAG_Int('SleepingX', 0),
                # nbt.TAG_Int('SleepingY', 0),
                # nbt.TAG_Int('SleepingZ', 0),
                nbt.TAG_List("Attributes", []),
            ],
        )

    def __str__(self) -> str:
        return self.username
