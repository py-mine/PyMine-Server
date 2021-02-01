from __future__ import annotations

import uuid

import pymine.types.nbt as nbt


class Player:
    def __init__(self, entity_id: int, data: nbt.TAG):
        self.entity_id = entity_id
        self.data = data

        self.uuid = uuid.UUID(bytes=struct.pack(">iiii", *data["uuid"]))
        self.x, self.y, self.z = self.pos = data["Pos"]
