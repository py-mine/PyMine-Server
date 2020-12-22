from __future__ import annotations
from nbt import nbt
import struct
import json
import uuid
import zlib

from src.data.registry import ITEMS_BY_NAME, ITEMS_BY_ID
from src.types.message import Message
from src.data.misc import *


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

    @classmethod
    def from_bytes(cls, data: bytes, comp_thresh: int = -1) -> Buffer:
        """
        Creates a Buffer object from bytes, handles compression
        and length prefixing
        """

        buf = cls(data)
        buf = cls(buf.read(buf.unpack_varint()))  # Handle length prefixing

        # Handle if the data was compressed
        if comp_thresh >= 0:
            uncomp_len = buf.unpack_varint()  # Handle decompressed length prefixing

            if uncomp_len > 0:
                # Create new Buffer from decompressed data
                buf = cls(zlib.decompress(buf.read()))

        return buf

    def to_bytes(self, comp_thresh: int = -1) -> bytes:
        """
        Packs the final Buffer into bytes, readies the data to be sent,
        handles compression and length prefixing.
        """

        if comp_thresh >= 0:
            if len(self.buf) >= comp_thresh:
                data = self.pack_varint(len(self.buf)) + zlib.compress(self.buf)
            else:
                data = self.pack_varint(0) + self.buf
        else:
            data = self.buf

        return self.pack_varint(len(data), max_bits=32) + data

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
            num |= (b & 0x7F) << (7 * i)

            if not b & 0x80:
                break

        if num & (1 << 31):
            num -= 1 << 32

        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(
                f'num doesn\'t fit in given range: {num_min} <= {num} < {num_max}')

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

        return uuid.to_bytes()

    def unpack_uuid(self):
        """Unpacks a UUID from the buffer."""

        return uuid.UUID(bytes=self.read(16))

    @classmethod
    def pack_msg(cls, msg: Message) -> bytes:
        """Packs a Minecraft chat message into bytes."""

        return msg.to_bytes()

    def unpack_msg(self) -> Message:
        """Unpacks a Minecraft chat message from the buffer."""

        return Message.from_buf(self)

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
    def pack_chat(cls, msg: Message) -> bytes:
        return msg.to_bytes()

    def unpack_chat(self):
        return Message.from_buf(self)

    @classmethod
    def pack_particle(cls, **particle):
        particle_id = particle['id']
        out = cls.pack_varint(particle_id)

        if particle_id in (3, 23,):
            out += cls.pack_varint(particle['BlockState'])
        elif particle_id == 14:
            out += cls.pack('ffff',
                            particle['Red'],
                            particle['Green'],
                            particle['Blue'],
                            particle['Scale'])
        elif particle_id == 32:
            out += cls.pack_slot(**particle['Item'])

        return out

    def unpack_particle(self):
        particle = {}
        particle_id = particle['id'] = self.unpack_varint()

        if particle_id in (3, 23,):
            particle['BlockState'] = cls.unpack_varint()
        elif particle_id == 14:
            particle['Red'] = cls.unpack('f')
            particle['Green'] = cls.unpack('f')
            particle['Blue'] = cls.unpack('f')
            particle['Scale'] = cls.unpack('f')
        elif particle_id == 32:
            particle['Item'] = cls.unpack_slot()

        return particle

    @classmethod
    # https://wiki.vg/Entity_metadata#Entity_Metadata_Format
    def pack_entity_metadata(cls, metadata: dict) -> bytes:
        """Packs entity metadata into bytes."""

        out = b''

        for index_and_type, value in metadata.items():
            index, type_ = index_and_type

            out += cls.pack('B', index) + cls.pack_varint(type_)

            if type_ == 0:
                out += cls.pack('b', value)
            elif type_ == 1:
                out += cls.pack_varint(value)
            elif type_ == 2:
                out += cls.pack('f', value)
            elif type_ == 3:
                out += cls.pack_string(value)
            elif type_ == 4:
                out += cls.pack_chat(value)
            elif type_ == 5:
                opt += cls.pack_bool((value is not None))

                if value is not None:
                    opt += cls.pack_chat(value)
            elif type_ == 6:
                out += cls.pack_slot(**value)
            elif type_ == 7:
                out += cls.pack_bool(value)
            elif type_ == 8:
                out += cls.pack_rotation(*value)
            elif type_ == 9:
                out += cls.pack_pos(*value)
            elif type_ == 10:
                out += cls.pack_bool((value is not None))

                if value is not None:
                    out += cls.pack_pos(*value)
            elif type_ == 11:
                out += cls.pack_direction(value)
            elif type_ == 12:
                out += cls.pack_bool((value is not None))

                if value is not None:
                    out += cls.pack_uuid(value)
            elif type_ == 13:
                out += cls.pack_bool((value is not None))

                if value is not None:
                    out += cls.pack_varint(value)
            elif type_ == 14:
                out += cls.pack_nbt(value)
            elif type_ == 15:
                out += cls.pack_particle(**value)
            elif type_ == 16:
                out += cls.pack_villager(*value)
            elif type_ == 17:
                out += cls.pack_optional_varint(value)
            elif type_ == 18:
                out += cls.pack_pose(value)

        return out + cls.pack('B', 255)

    def unpack_entity_metadata(self) -> dict:
        """Unpacks entity metadata from the buffer."""

        metadata = {}

        while True:
            index = self.unpack('B')

            if index == 255:
                return metadata

            type_ = self.unpack_varint()
            index_and_type = (index, type_,)

            if type_ == 0:
                metadata[index_and_type] = self.unpack('b')
            elif type_ == 1:
                metadata[index_and_type] = self.unpack_varint()
            elif type_ == 2:
                metadata[index_and_type] = self.unpack('f')
            elif type_ == 3:
                metadata[index_and_type] = self.unpack_string()
            elif type_ == 4:
                metadata[index_and_type] = self.unpack_chat()
            elif type_ == 5:
                if self.unpack_bool():
                    metadata[index_and_type] = self.unpack_chat()
            elif type_ == 6:
                metadata[index_and_type] = self.unpack_slot()
            elif type_ == 7:
                metadata[index_and_type] = self.unpack_bool()
            elif type_ == 8:
                metadata[index_and_type] = self.unpack_rotation()
            elif type_ == 9:
                metadata[index_and_type] = self.unpack_pos()
            elif type_ == 10:
                if self.unpack_bool():
                    metadata[index_and_type] = self.unpack_pos()
            elif type_ == 11:
                metadata[index_and_type] = self.unpack_direction()
            elif type_ == 12:
                if self.unpack_bool():
                    metadata[index_and_type] = self.unpack_uuid()
            elif type_ == 13:
                if self.unpack_bool():
                    metadata[index_and_type] = self.unpack_varint()
            elif type_ == 14:
                metadata[index_and_type] = self.unpack_nbt()
            elif type_ == 15:
                metadata[index_and_type] = self.unpack_particle()
            elif type_ == 16:
                metadata[index_and_type] = self.unpack_villager()
            elif type_ == 17:
                metadata[index_and_type] = self.unpack_optional_varint()
            elif type_ == 18:
                metadata[index_and_type] = self.unpack_pose()
