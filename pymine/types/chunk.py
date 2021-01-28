from __future__ import annotations

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class Chunk:
    def __init__(self, chunk_x: int, chunk_z: int, tag: nbt.TAG) -> None:
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.tag = tag
