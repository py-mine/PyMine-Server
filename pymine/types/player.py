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

    def __str__(self) -> str:
        return self.username
