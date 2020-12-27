from __future__ import annotations
from nbt import nbt
import struct
import json
import uuid
import zlib

from src.data.registry import ITEMS_BY_NAME, ITEMS_BY_ID
from src.types.packet import Packet
from src.data.misc import *

from src.util.share import logger


class Buffer:
    """
    Base class for a buffer, contains methods
    for handling most basic types and for
    converting from/to a Buffer object itself.
    """

    def __init__(self, buf: bytes = None) -> None:
        self.buf = b'' if buf is None else buf
        self.pos = 0

    def write(self, data: bytes) -> None:
        """Writes data to the buffer."""

        self.buf += data

    def read(self, length: int = None) -> bytes:
        """
        Reads n bytes from the buffer, if the length is None
        then all remaining data from the buffer is sent.
        """

        try:
            if length is None:
                length = len(self.buf)
                return self.buf[self.pos:]
            else:
                return self.buf[self.pos:self.pos + length]
        finally:
            self.pos += length

    def reset(self) -> None:
        """Resets the position in the buffer."""

        self.pos = 0

    @classmethod
    def pack_packet(cls, packet: Packet, comp_thresh: int = -1) -> bytes:  # nopep8
        """
        Packs a Packet object into bytes.
        """

        logger.debug(
            f'OUT: state:unknown     | id:{hex(packet.id_):<4} | packet:{type(packet).__name__}'
        )

        data = cls.pack_varint(packet.id_) + packet.encode()

        if comp_thresh >= 1:
            if len(data) >= comp_thresh:
                data = cls.pack_varint(len(data)) + zlib.compress(data)
            else:
                data = cls.pack_varint(0) + data

        return cls.pack_varint(len(data)) + data

    def unpack_packet(self, state: str, to: int, PACKET_MAP: object, comp_thresh: int = -1) -> Packet:  # nopepe8
        data = self.buf

        if comp_thresh >= 0:
            uncomp_len = self.unpack_varint()

            if uncom_len > 0:
                data = zlib.decompress(self.read())

        packet = PACKET_MAP[state][(self.unpack_varint(), to,)].decode(self)
        return packet

    def unpack(self, f: str) -> object:
        unpacked = struct.unpack('>' + f, self.read(struct.calcsize(f)))

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked

    @classmethod
    def pack(self, f: str, *data: object) -> bytes:
        return struct.pack('>' + f, *data)

    @classmethod
    def pack_bool(cls, boolean: bool) -> bytes:
        """Packs a boolean into bytes."""

        return struct.pack(f'>?', boolean)

    def unpack_bool(self) -> bool:
        """Unpacks a boolean from the buffer."""

        return self.unpack('?')

    @classmethod
    def pack_varint(cls, num: int, max_bits: int = 32) -> bytes:
        """Packs a varint (Varying Integer) into bytes."""

        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(
                f'num doesn\'t fit in given range: {num_min} <= {num} < {num_max}')

        if num < 0:
            num += 1 + 1 << 32

        out = b''

        for i in range(10):
            b = num & 0x7F
            num >>= 7

            out += cls.pack('B', (b | (0x80 if num > 0 else 0)))

            if num == 0:
                break

        return out

    def unpack_varint(self, max_bits: int = 32) -> int:
        """Unpacks a varint from the buffer."""

        num = 0

        for i in range(10):
            b = self.unpack('B')
            num |= (b & 0x7F) << 7 * i

            if not b & 0x80:
                break

        if num & (1 << 31):
            num -= 1 << 32

        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(f'num doesn\'t fit in given range: {num_min} <= {num} < {num_max}')

        return num

    @classmethod
    def pack_optional_varint(cls, num):
        """Packs an optional varint into bytes."""

        return cls.pack_varint(0 if num is None else num + 1)

    def unpack_optional_varint(cls):
        num = cls.unpack_varint()

        if num == 0:
            return None

        return num - 1

    @classmethod
    def pack_array(cls, f: str, array: list) -> bytes:
        """Packs an array/list into bytes."""

        return struct.pack(f'>{f*len(array)}', *array)

    @classmethod
    def pack_string(cls, text: str) -> bytes:
        """Packs a string into bytes."""

        text = text.encode('utf-8')
        return cls.pack_varint(len(text), max_bits=16) + text

    def unpack_string(self) -> str:
        """Unpacks a string from the buffer."""

        length = self.unpack_varint(max_bits=16)
        return self.read(length).decode('utf-8')

    def unpack_array(self, f: str, length: int) -> list:
        """Unpacks an array/list from the buffer."""

        data = self.read(struct.calcsize(f'>{f}') * length)
        return list(struct.unpack(f'>{f*length}', data))

    @classmethod
    def pack_json(cls, obj: object) -> bytes:
        """Packs json serializable data into bytes."""

        return cls.pack_string(json.dumps(obj))

    def unpack_json(self) -> object:
        """Unpacks serialized json data from the buffer."""

        return json.loads(self.unpack_string())

    @classmethod
    def pack_nbt(cls, tag: nbt.TAG = None) -> bytes:
        """Packs an NBT tag into bytes."""

        if tag is None:
            return b'\x00'

        return tag._render_buffer(cls.buf)

    def unpack_nbt(self) -> object:
        """Unpacks a NBT tag(s) from the buffer"""

        # assumes data is NOT compressed, isn't an issue (hopefully)!
        return nbt.NBTFile(buffer=self.buf)

    @classmethod
    def pack_uuid(cls, uuid: uuid.UUID) -> bytes:
        """Packs a UUID into bytes."""

        return uuid.bytes

    def unpack_uuid(self):
        """Unpacks a UUID from the buffer."""

        return uuid.UUID(bytes=self.read(16))

    @classmethod
    def pack_chat(cls, msg: 'Chat') -> bytes:
        """Packs a Minecraft chat message into bytes."""

        return cls.pack_json(msg.msg)

    def unpack_chat(self) -> 'Chat':
        """Unpacks a Minecraft chat message from the buffer."""

        return Chat.from_buf(self)

    @classmethod
    def pack_pos(cls, x, y, z) -> bytes:
        """Packs a Minecraft position (x, y, z) into bytes."""

        def to_twos_complement(num, bits):
            return num + (1 << bits) if num < 0 else num

        return struct.pack('>Q', sum((
            to_twos_complement(x, 26) << 38,
            to_twos_complement(z, 26) << 12,
            to_twos_complement(y, 12)
        )))

    def unpack_pos(self) -> tuple:
        """Unpacks a Minecraft position (x, y, z) from the buffer."""

        def from_twos_complement(num, bits):
            if num & (1 << (bits - 1)) != 0:
                num -= (1 << bits)

            return num

        data = self.unpack('Q')

        x = from_twos_complement(data >> 38, 26)
        z = from_twos_complement(data >> 12 & 0x3FFFFFF, 26)
        y = from_twos_complement(data & 0xFFF, 12)

        return x, y, z

    @classmethod
    def pack_slot(cls, item: str = None, count: int = 1, tag: nbt.TAG = None):
        """Packs an inventory/container slot into bytes."""

        item_id = ITEMS_BY_NAME[item]  # needed to support recipes

        if item_id is None:
            return cls.pack('?', False)

        return cls.pack('?', True) + cls.pack_varint(item_id) + \
            cls.pack('b', count) + cls.pack_nbt(tag)

    def unpack_slot(self):
        """Unpacks an inventory/container slot from the buffer."""

        has_item_id = self.unpack_optional()

        if not has_item_id:
            return {'item': None}

        return {
            'item': ITEMS_BY_ID[self.unpack_varint()],
            'count': self.unpack('b'),
            'tag': self.unpack_nbt()
        }

    @classmethod
    def pack_rotation(cls, x: float, y: float, z: float) -> bytes:
        """Packs a rotation (of an entity) into bytes."""

        return cls.pack('fff', x, y, z)

    def unpack_rotation(self):
        """Unpacks a rotation (of an entity) from the buffer."""

        return self.unpack('fff')

    @classmethod
    def pack_direction(cls, direction: str) -> bytes:
        """Packs a direction into bytes."""

        return cls.pack_varint(DIRECTIONS.index(direction))

    def unpack_direction(self) -> str:
        """Unpacks a direction from the buffer."""

        return DIRECTIONS[self.unpack_varint()]

    @classmethod
    def pack_pose(cls, pose: str) -> bytes:
        """Packs a pose into bytes."""

        return cls.pack_varint(POSES.index(pose))

    def unpack_pose(self) -> str:
        """Unpacks a pose from the buffer."""

        return POSES[self.unpack_varint()]

    @classmethod
    def pack_ingredient(cls, ingredient: object) -> bytes:
        """Packs a recipe ingredient into bytes."""

        out = b''

        if isinstance(ingredient, list):
            out += cls.pack_varint(len(ingredient))
            for slot in ingredient:
                out += cls.pack_slot(**slot)
        elif isinstance(ingredient, dict):
            out += cls.pack_varint(1)
            out += cls.pack_slot(**ingredient)
        else:
            raise TypeError(
                f'Ingredient should be of type list or dict but was instead of type {type(ingredient)}')

        return out

    # def unpack_ingredient(self):
    #     """Unpacks a recipe ingredient from the buffer."""
    #
    #     return [self.unpack_slot() for _ in range(self.unpack_varint())]

    @classmethod  # Note, recipes are sent as an array and actually require a varint length of recipe array before recipe array
    # recipe_id is the actual name of the recipe i.e. jungle_planks, oak_door, furnace, etc...
    def pack_recipe(cls, recipe_id: str, recipe: dict) -> bytes:  # https://wiki.vg/Protocol#Declare_Recipes
        """Packs a recipe into bytes."""

        # ------------------------------- shapeless recipe -------------------------------
        # {
        #   "type": "minecraft:crafting_shapeless",  # Type of crafting recipe, see here: https://wiki.vg/Protocol#Declare_Recipes
        #   "group": "dyed_bed",  # Crafting group, used for recipe unlocks among other things
        #   "ingredients": [  # Each of these are "slots"
        #     {
        #       "item": "minecraft:white_bed"
        #     },
        #     {
        #       "item": "minecraft:black_dye"
        #     }
        #   ],
        #   "result": {  # Result item of recipe, should be packed as a slot
        #     "item": "minecraft:black_bed"
        #   }
        # }
        # ------------------------------- shaped recipe -------------------------------
        # {
        #   "type": "minecraft:crafting_shaped",
        #   "group": "sign",  # Crafting group
        #   "pattern": [  # Pattern layed out for recipe
        #     "###",
        #     "###",
        #     " X "
        #   ],
        #   "key": {  # Which character in the pattern corresponds to what item, each of these should be slots
        #     "#": {
        #       "item": "minecraft:acacia_planks"
        #     },
        #     "X": {
        #       "item": "minecraft:stick"
        #     }
        #   },
        #   "result": {  # Result of the recipe, should be packed as a slot
        #     "item": "minecraft:acacia_sign",
        #     "count": 3
        #   }
        # }

        recipe_type = recipe['type']

        out = cls.pack_string(recipe_type) + cls.pack_string(recipe_id)

        if recipe_type == 'minecraft:crafting_shapeless':
            out += cls.pack_string(recipe['group'])
            out += cls.pack_varint(len(recipe['ingredients']))  # Length of ingredient array

            for ingredient in recipe['ingredients']:
                out += self.pack_ingredient(ingredient)

            out += cls.pack_slot(**recipe['result'])
        elif recipe_type == 'minecraft:crafting_shaped':
            width = len(recipe['pattern'][0])  # Width of pattern
            height = len(recipe['pattern'])  # Height of pattern

            out += cls.pack_varint(width)
            out += cls.pack_varint(height)
            out += cls.pack_string(recipe['group'])

            out += cls.pack_varint(width * height)  # pack length of ingredients array

            for row in recipe['pattern']:
                for key in row:
                    if recipe['key'][key].get('item'):
                        out += cls.pack_ingredient(recipe['key'][key])

            out += cls.pack_slot(**recipe['result'])
        elif recipe_type in SMELT_TYPES:  # SMELT_TYPES imported from misc.py
            out += cls.pack_string(recipe['group'])
            out += cls.pack_ingredient(recipe['ingredient'])
            out += cls.pack_slot(**recipe['result'])
            out += cls.pack('f', recipe['experience'])
            out += cls.pack_varint(recipe['cookingtime'])
        elif recipe_type == 'minecraft:stonecutting':  # Stone cutter recipes are fucky wucky, so we have to do some jank here
            # For some reason some recipes don't include the group?
            out += cls.pack_string(recipe.get('group', ''))
            out += cls.pack_ingredient(recipe['ingredient'])
            # again, stone cutter recipes are fucky wucky
            out += cls.pack_slot(item=recipe['result'], count=recipe['count'])
        elif recipe_type == 'minecraft:smithing':
            out += cls.pack_ingredient(recipe['base'])
            out += cls.pack_ingredient(recipe['addition'])
            out += cls.pack_slot(**recipe['result'])

        return out

    @classmethod
    def pack_villager(cls, kind: int, profession: int, level: int) -> bytes:
        """Packs villager data into bytes."""

        return cls.pack_varint(kind) + cls.pack_varint(profession) + cls.pack_varint(level)

    def unpack_villager(self) -> dict:
        """Unpacks villager data from the buffer."""

        return {
            'kind': self.unpack_varint(),
            'profession': self.unpack_varint(),
            'level': self.unpack_varint()
        }
