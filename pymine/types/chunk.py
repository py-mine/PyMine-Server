from __future__ import annotations

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class Chunk:
    def __init__(self, tag: nbt.TAG, timestamp: int) -> None:
        self.tag = tag
        self.timestamp = timestamp
