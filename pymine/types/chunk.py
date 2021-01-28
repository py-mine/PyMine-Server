from __future__ import annotations

from pymine.types.buffer import Buffer
import pymine.types.nbt as nbt


class Chunk(dict):
    def __init__(self, tag: nbt.TAG, timestamp: int) -> None:
        dict.__init__(self, tag['Level'])

        self.data_version = tag["DataVersion"]

        self.chunk_x = self["xPos"].data
        self.chunk_z = self["zPos"].data

        self.timestamp = timestamp
