"""Contains packets related to the in-game map item."""

from __future__ import annotations

from src.types.packet import Packet
from src.types.buffer import Buffer
from src.types.chat import Chat

# __all__ = ('PlayMapData',)


class PlayMapData(Packet):
    """Insert fancy shmancy docstring"""

    id = 0x25
    to = 1

    def __init__(
            self,
            map_id: int,
            scale: int,
            tracking_pos: bool,
            locked: bool,
            icons: list,
            cols: int,
            rows: int = None,
            x: int = None,
            z: int = None,
            data: bytes = None) -> None:
        super().__init__()

        self.map_id = map_id
        self.scale = scale
        self.tracking_pos = tracking_pos
        self.locked = locked
        self.icons = icons
        self.cols = cols
        self.rows = rows
        self.x, self.z = x, z
        self.data = data

    def encode(self) -> bytes:
        out = Buffer.pack_varint(self.map_id) + Buffer.pack('b', self.scale) + Buffer.pack('?', self.tracking_pos) + \
            Buffer.pack('?', self.locked) + Buffer.pack_varint(len(self.icons))

        for icon in self.icons:
            out += Buffer.pack_varint(icon['type']) + Buffer.pack('b', icon['x']) + Buffer.pack('b', icon['z'])

            display_name = icon.get('display_name')

            if display_name is not None:
                out += Buffer.pack('?', True) + Buffer.pack_chat(Chat(display_name))
            else:
                out += Buffer.pack('?', False)

        out += Buffer.pack('B', self.cols)

        raise NotImplementedError
