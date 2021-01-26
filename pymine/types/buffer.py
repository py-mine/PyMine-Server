from __future__ import annotations
from nbt import nbt
import struct
import json
import uuid
import zlib

from pymine.types.packet import Packet
from pymine.types.chat import Chat

from pymine.data.registry import ITEM_REGISTRY
import pymine.data.misc as misc_data


class Buffer:
    """
    Base class for a buffer, contains methods
    for handling most basic types and for
    converting from/to a Buffer object itself.
    """

    def __init__(self, buf: bytes = None) -> None:
        self.buf = b"" if buf is None else buf
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
                return self.buf[self.pos :]

            return self.buf[self.pos : self.pos + length]
        finally:
            self.pos += length

    def reset(self) -> None:
        """Resets the position in the buffer."""

        self.pos = 0

    @classmethod
    def pack_packet(cls, packet: Packet, comp_thresh: int = -1) -> bytes:
        """
        Packs a Packet object into bytes.
        """

        data = cls.pack_varint(packet.id) + packet.encode()

        if comp_thresh >= 1:
            if len(data) >= comp_thresh:
                data = cls.pack_varint(len(data)) + zlib.compress(data)
            else:
                data = cls.pack_varint(0) + data

        return cls.pack_varint(len(data)) + data

    def unpack_packet(self, state: str, PACKET_MAP: object, comp_thresh: int = -1) -> Packet:
        data = self.buf

        if comp_thresh >= 0:
            uncomp_len = self.unpack_varint()

            if uncomp_len > 0:
                data = zlib.decompress(self.read())

        return PACKET_MAP[state][self.unpack_varint()].decode(self)

    def unpack(self, f: str) -> object:
        unpacked = struct.unpack(">" + f, self.read(struct.calcsize(f)))

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked

    @classmethod
    def pack(self, f: str, *data: object) -> bytes:
        return struct.pack(">" + f, *data)

    @classmethod
    def pack_optional(cls, packer: object, data: object = None) -> bytes:
        """Packs an optional field into bytes."""

        if data is None:
            return cls.pack("?", False)

        return cls.pack("?", True) + packer(data)

    def unpack_optional(self, unpacker: object) -> bool:
        """Unpacks an optional field from the buffer."""

        present = self.unpack("?")

        if present:
            return unpacker()

    @classmethod
    def pack_varint(cls, num: int, max_bits: int = 32) -> bytes:
        """Packs a varint (Varying Integer) into bytes."""

        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(f"num doesn't fit in given range: {num_min} <= {num} < {num_max}")

        if num < 0:
            num += 1 + 1 << 32

        out = b""

        for i in range(10):
            b = num & 0x7F
            num >>= 7

            out += cls.pack("B", (b | (0x80 if num > 0 else 0)))

            if num == 0:
                break

        return out

    def unpack_varint(self, max_bits: int = 32) -> int:
        """Unpacks a varint from the buffer."""

        num = 0

        for i in range(10):
            b = self.unpack("B")
            num |= (b & 0x7F) << 7 * i

            if not b & 0x80:
                break

        if num & (1 << 31):
            num -= 1 << 32

        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(f"num doesn't fit in given range: {num_min} <= {num} < {num_max}")

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

        return struct.pack(f">{f*len(array)}", *array)

    def unpack_array(self, f: str, length: int) -> list:
        """Unpacks an array/list from the buffer."""

        data = self.read(struct.calcsize(f">{f}") * length)
        return list(struct.unpack(f">{f*length}", data))

    @classmethod
    def pack_string(cls, text: str) -> bytes:
        """Packs a string into bytes."""

        text = text.encode("utf-8")
        return cls.pack_varint(len(text), max_bits=16) + text

    def unpack_string(self) -> str:
        """Unpacks a string from the buffer."""

        length = self.unpack_varint(max_bits=16)
        return self.read(length).decode("utf-8")

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
            return b"\x00"

        buf = cls()
        tag._render_buffer(buf)
        return buf.buf

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
    def pack_chat(cls, msg: Chat) -> bytes:
        """Packs a Minecraft chat message into bytes."""

        return cls.pack_json(msg.msg)

    def unpack_chat(self) -> Chat:
        """Unpacks a Minecraft chat message from the buffer."""

        return Chat(self.unpack_json())

    @classmethod
    def pack_pos(cls, x: int, y: int, z: int) -> bytes:
        """Packs a Minecraft position (x, y, z) into bytes."""

        def to_twos_complement(num, bits):
            return num + (1 << bits) if num < 0 else num

        return struct.pack(
            ">Q", sum((to_twos_complement(x, 26) << 38, to_twos_complement(z, 26) << 12, to_twos_complement(y, 12)))
        )

    def unpack_pos(self) -> tuple:
        """Unpacks a Minecraft position (x, y, z) from the buffer."""

        def from_twos_complement(num, bits):
            if num & (1 << (bits - 1)) != 0:
                num -= 1 << bits

            return num

        data = self.unpack("Q")

        x = from_twos_complement(data >> 38, 26)
        z = from_twos_complement(data >> 12 & 0x3FFFFFF, 26)
        y = from_twos_complement(data & 0xFFF, 12)

        return x, y, z

    @classmethod
    def pack_slot(cls, item: str = None, count: int = 1, tag: nbt.TAG = None):
        """Packs an inventory/container slot into bytes."""

        item_id = ITEM_REGISTRY.encode(item)  # needed to support recipes

        if item_id is None:
            return cls.pack("?", False)

        return cls.pack("?", True) + cls.pack_varint(item_id) + cls.pack("b", count) + cls.pack_nbt(tag)

    def unpack_slot(self):
        """Unpacks an inventory/container slot from the buffer."""

        has_item_id = self.unpack_optional()

        if not has_item_id:
            return {"item": None}

        return {"item": ITEM_REGISTRY.decode(self.unpack_varint()), "count": self.unpack("b"), "tag": self.unpack_nbt()}

    @classmethod
    def pack_rotation(cls, x: float, y: float, z: float) -> bytes:
        """Packs a rotation (of an entity) into bytes."""

        return cls.pack("fff", x, y, z)

    def unpack_rotation(self):
        """Unpacks a rotation (of an entity) from the buffer."""

        return self.unpack("fff")

    @classmethod
    def pack_direction(cls, direction: str) -> bytes:
        """Packs a direction into bytes."""

        return cls.pack_varint(misc_data.DIRECTIONS.index(direction))

    def unpack_direction(self) -> str:
        """Unpacks a direction from the buffer."""

        return misc_data.DIRECTIONS[self.unpack_varint()]

    @classmethod
    def pack_pose(cls, pose: str) -> bytes:
        """Packs a pose into bytes."""

        return cls.pack_varint(misc_data.POSES.index(pose))

    def unpack_pose(self) -> str:
        """Unpacks a pose from the buffer."""

        return misc_data.POSES[self.unpack_varint()]

    @classmethod
    def pack_ingredient(cls, ingredient: object) -> bytes:
        """Packs a recipe ingredient into bytes."""

        if isinstance(ingredient, list):
            return cls.pack_varint(len(ingredient)) + b"".join([cls.pack_slot(**slot) for slot in ingredient])

        if isinstance(ingredient, dict):
            return cls.pack_varint(1) + cls.pack_slot(**ingredient)

        raise TypeError(f"Ingredient should be of type list or dict but was instead of type {type(ingredient)}")

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

        recipe_type = recipe["type"]

        out = cls.pack_string(recipe_type) + cls.pack_string(recipe_id)

        if recipe_type == "minecraft:crafting_shapeless":
            out += cls.pack_string(recipe["group"])
            out += cls.pack_varint(len(recipe["ingredients"]))  # Length of ingredient array
            out += b"".join([cls.pack_ingredient(ingredient) for ingredient in recipe["ingredients"]])
            out += cls.pack_slot(**recipe["result"])
        elif recipe_type == "minecraft:crafting_shaped":
            width = len(recipe["pattern"][0])  # Width of pattern
            height = len(recipe["pattern"])  # Height of pattern

            out += cls.pack_varint(width)
            out += cls.pack_varint(height)
            out += cls.pack_string(recipe["group"])

            out += cls.pack_varint(width * height)  # pack length of ingredients array

            for row in recipe["pattern"]:
                for key in row:
                    if recipe["key"][key].get("item"):
                        out += cls.pack_ingredient(recipe["key"][key])

            out += cls.pack_slot(**recipe["result"])
        elif recipe_type in misc_data.SMELT_TYPES:  # SMELT_TYPES imported from misc.py
            out += cls.pack_string(recipe["group"])
            out += cls.pack_ingredient(recipe["ingredient"])
            out += cls.pack_slot(**recipe["result"])
            out += cls.pack("f", recipe["experience"])
            out += cls.pack_varint(recipe["cookingtime"])
        elif recipe_type == "minecraft:stonecutting":  # Stone cutter recipes are fucky wucky, so we have to do some jank here
            # For some reason some recipes don't include the group?
            out += cls.pack_string(recipe.get("group", ""))
            out += cls.pack_ingredient(recipe["ingredient"])
            # again, stone cutter recipes are fucky wucky
            out += cls.pack_slot(item=recipe["result"], count=recipe["count"])
        elif recipe_type == "minecraft:smithing":
            out += cls.pack_ingredient(recipe["base"])
            out += cls.pack_ingredient(recipe["addition"])
            out += cls.pack_slot(**recipe["result"])

        return out

    @classmethod
    def pack_villager(cls, kind: int, profession: int, level: int) -> bytes:
        """Packs villager data into bytes."""

        return cls.pack_varint(kind) + cls.pack_varint(profession) + cls.pack_varint(level)

    def unpack_villager(self) -> dict:
        """Unpacks villager data from the buffer."""

        return {"kind": self.unpack_varint(), "profession": self.unpack_varint(), "level": self.unpack_varint()}

    @classmethod
    def pack_trade(
        cls,
        in_item_1: dict,
        out_item: dict,
        disabled: bool,
        num_trade_usages: int,
        max_trade_usages: int,
        xp: int,
        special_price: int,
        price_multi: float,
        demand: int,
        in_item_2: dict = None,
    ) -> bytes:
        out = Buffer.pack_slot(**in_item_1) + Buffer.pack_slot(**out_item)

        if in_item_2 is not None:
            out += Buffer.pack("?", True) + Buffer.pack_slot(**in_item_2)
        else:
            out += Buffer.pack("?", False)

        return (
            out
            + Buffer.pack("?", disabled)
            + Buffer.pack("i", num_trade_usages)
            + Buffer.pack("i", max_trade_usages)
            + Buffer.pack("i", xp)
            + Buffer.pack("i", special_price)
            + Buffer.pack("f", price_multi)
            + Buffer.pack("i", demand)
        )

    @classmethod
    def pack_particle(cls, **particle):
        particle_id = particle["id"]
        out = cls.pack_varint(particle_id)

        if particle_id in (
            3,
            23,
        ):
            out += cls.pack_varint(particle["block_state"])
        elif particle_id == 14:
            out += cls.pack("ffff", particle["red"], particle["green"], particle["blue"], particle["scale"])
        elif particle_id == 32:
            out += cls.pack_slot(**particle["item"])

        return out

    def unpack_particle(self):
        particle = {}
        particle_id = particle["id"] = self.unpack_varint()

        if particle_id in (
            3,
            23,
        ):
            particle["block_state"] = self.unpack_varint()
        elif particle_id == 14:
            particle["red"] = self.unpack("f")
            particle["green"] = self.unpack("f")
            particle["blue"] = self.unpack("f")
            particle["scale"] = self.unpack("f")
        elif particle_id == 32:
            particle["item"] = self.unpack_slot()

        return particle

    @classmethod
    def pack_entity_metadata(cls, metadata: dict) -> bytes:
        out = b""

        for index_and_type, value in metadata.items():
            index, type_ = index_and_type

            out += cls.pack("B", index) + cls.pack_varint(type_)

            if type_ == 0:  # byte
                out += cls.pack("b", value)
            elif type_ == 1:  # varint
                out += cls.pack_varint(value)
            elif type_ == 2:  # float
                out += cls.pack("f", value)
            elif type_ == 3:  # string
                out += cls.pack_string(value)
            elif type_ == 4:  # Chat
                out += cls.pack_chat(value)
            elif type_ == 5:  # optional Chat
                out += cls.pack_optional(cls.pack_chat, value)
            elif type_ == 6:  # Slot
                out += cls.pack_slot(**value)
            elif type_ == 7:  # bool
                out += cls.pack("?", value)
            elif type_ == 8:  # rotation
                out += cls.pack_rotation(*value)
            elif type_ == 9:  # position
                out += cls.pack_pos(*value)
            elif type_ == 10:  # optional position
                if value is not None:
                    out += cls.pack_bool("?", True) + cls.pack_pos(*value)
                else:
                    out += cls.pack_bool("?", False)
            elif type_ == 11:  # direction
                out += cls.pack_direction(value)
            elif type_ == 12:  # optional uuid
                out += cls.pack_optional(cls.pack_uuid, value)
            elif type_ == 13:  # optional block id
                out += cls.pack_optional(cls.pack_optional, value)
            elif type_ == 14:  # NBT
                out += cls.pack_nbt(value)
            elif type_ == 15:  # particle
                out += cls.pack_particle(value)
            elif type_ == 16:  # villager data
                out += cls.pack_villager(*value)
            elif type_ == 17:  # optional varint
                out += cls.pack_optional_varint(value)
            elif type_ == 18:  # pose
                out += cls.pack_pose(value)

        return out + b"\xFE"
