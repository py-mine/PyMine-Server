from __future__ import annotations
import immutables
import struct
import json
import uuid
import zlib

from pymine.types.block_palette import DirectPalette
from pymine.types.chunk import Chunk, ChunkSection
from pymine.types.bitfield import BitField
from pymine.types.packet import Packet
from pymine.types.chat import Chat
import pymine.types.nbt as nbt

from pymine.data.registries import ITEM_REGISTRY
import pymine.data.misc as misc_data
from pymine.data.tags import TAGS

from pymine.api.errors import InvalidPacketID
from pymine.types.abc import AbstractPalette


class Buffer:
    """
    Base class for a buffer, contains methods
    for handling most basic types and for
    converting from/to a Buffer object itself.
    """

    def __init__(self, buf: bytes = None) -> None:
        self.buf = b"" if buf is None else buf
        self.pos = 0

    def __len__(self):
        return len(self.buf)

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

    def unpack_byte(self) -> int:
        byte = self.buf[self.pos]
        self.pos += 1
        return byte

    @classmethod
    def pack_byte(cls, b: int) -> bytes:
        return struct.pack(">b", b)

    def reset(self) -> None:
        """Resets the position in the buffer."""

        self.pos = 0

    def unpack(self, f: str) -> object:
        unpacked = struct.unpack(">" + f, self.read(struct.calcsize(f)))

        if len(unpacked) == 1:
            return unpacked[0]

        return unpacked

    @classmethod
    def pack(cls, f: str, *data: object) -> bytes:
        return struct.pack(">" + f, *data)

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

        try:
            packet_class = PACKET_MAP[state][self.unpack_varint()]
        except KeyError:
            raise InvalidPacketID

        return packet_class.decode(self)

    @classmethod
    def pack_optional(cls, packer: object, data: object = None) -> bytes:
        """Packs an optional field into bytes."""

        if data is None:
            return cls.pack("?", False)

        return cls.pack("?", True) + packer(data)

    def unpack_optional(self, unpacker: object) -> object:
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

        return tag.pack()

    def unpack_nbt(self):
        return nbt.unpack(self)

    @classmethod
    def pack_uuid(cls, uuid_: uuid.UUID) -> bytes:
        """Packs a UUID into bytes."""

        return uuid_.bytes

    def unpack_uuid(self) -> uuid.UUID:
        """Unpacks a UUID from the buffer."""

        return uuid.UUID(bytes=self.read(16))

    @classmethod
    def pack_chat(cls, msg: Chat) -> bytes:
        """Packs a Minecraft chat message into bytes."""

        if isinstance(msg, Chat):
            return cls.pack_json(msg.msg)

        return cls.pack_json(Chat(msg).msg)

    def unpack_chat(self) -> Chat:
        """Unpacks a Minecraft chat message from the buffer."""

        return Chat(self.unpack_json())

    @classmethod
    def pack_position(cls, x: int, y: int, z: int) -> bytes:
        """Packs a Minecraft position (x, y, z) into bytes."""

        def to_twos_complement(num, bits):
            return num + (1 << bits) if num < 0 else num

        return struct.pack(
            ">Q", sum((to_twos_complement(x, 26) << 38, to_twos_complement(z, 26) << 12, to_twos_complement(y, 12)))
        )

    def unpack_position(self) -> tuple:
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
    def pack_slot(cls, item: str = None, count: int = 1, tag: nbt.TAG = None) -> bytes:
        """Packs an inventory/container slot into bytes."""

        item_id = ITEM_REGISTRY.encode(item)  # needed to support recipes

        if item_id is None:
            return cls.pack("?", False)

        return cls.pack("?", True) + cls.pack_varint(item_id) + cls.pack("b", count) + cls.pack_nbt(tag)

    def unpack_slot(self) -> dict:
        """Unpacks an inventory/container slot from the buffer."""

        has_item_id = self.unpack_optional()

        if not has_item_id:
            return {"item": None}

        return {"item": ITEM_REGISTRY.decode(self.unpack_varint()), "count": self.unpack("b"), "tag": self.unpack_nbt()}

    @classmethod
    def pack_rotation(cls, x: float, y: float, z: float) -> bytes:
        """Packs a rotation (of an entity) into bytes."""

        return cls.pack("fff", x, y, z)

    def unpack_rotation(self) -> tuple:
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
    def pack_positione(cls, pose: str) -> bytes:
        """Packs a pose into bytes."""

        return cls.pack_varint(misc_data.POSES.index(pose))

    def unpack_positione(self) -> str:
        """Unpacks a pose from the buffer."""

        return misc_data.POSES[self.unpack_varint()]

    @classmethod
    def pack_recipe_item(cls, item):
        if isinstance(item, (dict, immutables.Map)):
            return cls.pack_slot(**item)

        if isinstance(item, str):
            return cls.pack_slot(item)

        raise TypeError(f"Invalid type {type(item)}.")

    @classmethod
    def pack_ingredient(cls, ingredient: dict) -> bytes:
        """Packs a recipe ingredient into bytes."""

        return cls.pack_varint(len(ingredient)) + b"".join([cls.pack_recipe_item(slot) for slot in ingredient.values()])

    @classmethod  # Note, recipes are sent as an array and actually require a varint length of recipe array before recipe array
    # recipe_id is the actual name of the recipe i.e. jungle_planks, oak_door, furnace, etc...
    def pack_recipe(cls, recipe_id: str, recipe: dict) -> bytes:  # https://wiki.vg/Protocol#Declare_Recipes
        """Packs a recipe into bytes."""

        type_ = recipe["type"]
        out = cls.pack_string(type_) + cls.pack_string(recipe_id)

        if recipe.get("group") is None:
            recipe = {**recipe, "group": "null"}

        if type_ == "minecraft:crafting_shapeless":
            print(recipe.get("ingredients"))
            out += (
                cls.pack_string(recipe["group"])
                + cls.pack_varint(len(recipe["ingredients"]))
                + b"".join([cls.pack_ingredient(ingredient) for ingredient in recipe.get("ingredients", [])])
                + cls.pack_recipe_item(recipe["result"])
            )
        elif type_ == "minecraft:crafting_shaped":
            out += (
                cls.pack_varint(len(recipe["pattern"][0]))
                + cls.pack_varint(len(recipe["pattern"]))
                + cls.pack_string(recipe["group"])
                + b"".join([cls.pack_ingredient(ingredient) for ingredient in recipe.get("ingredients", [])])
                + cls.pack_recipe_item(recipe["result"])
            )
        elif type_[10:] in ("smelting", "blasting", "campfire_cooking"):
            print(recipe)

            out += (
                cls.pack_string(recipe["group"])
                + cls.pack_ingredient(recipe["ingredient"])
                + cls.pack_recipe_item(recipe["result"])
                + cls.pack("f", recipe["experience"])
                + cls.pack_varint(recipe["cookingtime"])
            )
        elif type_ == "minecraft:stonecutting":
            out += (
                cls.pack_string(recipe["group"])
                + cls.pack_ingredient(recipe["ingredient"])
                + cls.pack_recipe_item(recipe["result"])
            )
        elif type_ == "minecraft:smithing":
            out += (
                cls.pack_ingredient(recipe["base"])
                + cls.pack_ingredient(recipe["addition"])
                + cls.pack_recipe_item(recipe["result"])
            )

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
    def pack_particle(cls, **particle) -> bytes:
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

    def unpack_particle(self) -> dict:
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
                out += cls.pack_position(*value)
            elif type_ == 10:  # optional position
                if value is not None:
                    out += cls.pack_bool("?", True) + cls.pack_position(*value)
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
                out += cls.pack_positione(value)

        return out + b"\xFE"

    # 0 = add/subtract amount, 1 = add/subtract amount percent of the current value, 2 = multiply by percent amount
    @classmethod
    def pack_modifier(cls, uuid_: uuid.UUID, amount: float, operation: int) -> bytes:
        return cls.pack_uuid(uuid_) + Buffer.pack("d", amount) + Buffer.pack("b", operation)

    def unpack_modifier(self) -> tuple:
        return self.unpack_uuid(), self.unpack("d"), self.unpack("b")

    @classmethod
    def pack_node(cls, node: dict) -> bytes:
        out = (
            cls.pack_byte(node["flags"])
            + cls.pack_varint(len(node["children"]))
            + b"".join([cls.pack_node(child) for child in node["children"]])
        )

        if node["flags"] & 0x08:
            out += cls.pack_varint(node["redirect_node"])

        if node["flags"] & 0x03 in (1, 2):  # argument or literal node
            out += cls.pack_string(node["name"])

        if node["flags"] & 0x03 == 2:  # argument node
            out += cls.pack_string(node["parser"])

            if node.get("properties"):
                for packer, data in node["properties"]:
                    out += packer(data)

        if node["flags"] & 0x10:
            out += cls.pack_string(node["suggestions_type"])

        return out

    @classmethod
    def pack_block_palette(cls, palette: AbstractPalette) -> bytes:
        if palette is DirectPalette:
            return b""

        return cls.pack_varint(len(palette.registry.data)) + b"".join(  # map indirect ids to the global palette
            [cls.pack_varint(DirectPalette.encode(palette.decode(state_id))) for state_id in range(len(palette.registry.data))]
        )

    @classmethod
    def pack_chunk_section_blocks(cls, section: ChunkSection) -> bytes:
        if section.block_states is None:
            return cls.pack_varint(0)  # length is 0
        else:
            palette = section.palette
            bits_per_block = palette.get_bits_per_block()

            # pack bits per block and palette
            out = cls.pack("b", bits_per_block) + cls.pack_block_palette(palette)

            data = [0] * int((16 * 16 * 16) * bits_per_block / 64)
            individual_value_mask = (1 << bits_per_block) - 1

            # create the long array from the block states
            for y in range(16):
                for z in range(16):
                    for x in range(16):
                        block_num = (((y * 16) + z) * 16) + x
                        start_long = (block_num * bits_per_block) // 64
                        start_offset = (block_num * bits_per_block) % 64
                        end_long = ((block_num + 1) * bits_per_block - 1) // 64

                        value = section.block_states[x][y][z] & individual_value_mask

                        data[start_long] |= value << start_offset

                        if start_long != end_long:
                            data[end_long] = value >> (64 - start_offset)

            # pack and return the block state long array
            return cls.pack_varint(len(data)) + b"".join([cls.pack("q", q) for q in data])

    @classmethod
    def pack_chunk_light(cls, chunk: Chunk) -> bytes:
        out = cls.pack_varint(chunk.x) + cls.pack_varint(chunk.z) + cls.pack("?", True)

        sky_light_mask = 0
        block_light_mask = 0
        empty_sky_light_mask = 0
        empty_block_light_mask = 0

        sky_light_arrays = []
        block_light_arrays = []

        for section_y in range(-1, 17, 1):
            section = chunk.get(section_y)

            section_y += 1

            if section is None:
                empty_sky_light_mask |= 1 << section_y
                empty_block_light_mask |= 1 << section_y

                continue

            if section.sky_light is None or len(section.sky_light.nonzero()) == 0:
                empty_sky_light_mask |= 1 << section_y
            else:
                sky_light_mask |= 1 << section_y

                sky_light_array = b""

                for y in range(16):
                    for z in range(16):
                        for x in range(0, 16, 2):
                            sky_light_array += cls.pack("B",
                                (section.sky_light[y][z][x] << 4) | section.sky_light[y][z][x+1]
                            )

                sky_light_arrays.append(cls.pack_varint(len(sky_light_array)) + sky_light_array)

            if section.block_light is None or len(section.block_light.nonzero()) == 0:
                empty_block_light_mask |= 1 << section_y
            else:
                block_light_mask |= 1 << section_y

                block_light_array = b""

                for y in range(16):
                    for z in range(16):
                        for x in range(0, 16, 2):
                            block_light_array += cls.pack("B",
                                (section.block_light[y][z][x] << 4) | section.block_light[y][z][x+1]
                            )

                block_light_arrays.append(cls.pack_varint(len(block_light_array)) + block_light_array)

        return (
            cls.pack_varint(sky_light_mask)
            + cls.pack_varint(block_light_mask)
            + cls.pack_varint(empty_sky_light_mask)
            + cls.pack_varint(empty_block_light_mask)
            + b"".join(sky_light_arrays)
            + b"".join(block_light_arrays)
        )
