from __future__ import annotations

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class Chunk:
    def __init__(self, tag: nbt.TAG, timestamp: int) -> None:
        self.data_version = tag['DataVersion']
        self.level = tag['Level']

        self.chunk_x = self.level['xPos']
        self.chunk_z = self.level['zPos']

        self.timestamp = timestamp
