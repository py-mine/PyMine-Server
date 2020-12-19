import struct
import json
import zlib


class Packet:
    def __init__(self):
        self.buf = b''
        self.pos = 0

    def add(self, data: bytes):
        self.buf += data

    def read(self, length: int = 1) -> bytes:
        try:
            return self.buf[self.pos:self.pos+length]
        finally:
            self.pos += length

    def reset(self) -> None:
        self.pos = 0

    @classmethod
    def pack_array(cls, f, array: list) -> bytes:
        return struct.pack(f'>{f*len(array)}', *array)

    def unpack_array(f, length: int) -> list:
        data = self.read(struct.calcsize(f'>{f}') * length)
        return list(struct.unpack(f'>{f*length}', data))

    @classmethod
    def pack_bool(cls, boolean) -> bytes:
        return struct.pack(f'>?', boolean)

    def unpack_bool(self) -> bool:
        return struct.unpack(f'>?', self.read(1))

    @classmethod
    def pack_varint(cls, num: int, max_bits: int = 32) -> bytes:
        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(f'num doesn\'t fit in given range: {num_min} <= {num} < {num_max}')

        if num < 0:
            num += 1 + 1 << 32

        out = b''

        for i in range(10):
            b = num & 0x7F
            num >>= 7

            out += struct.pack('>B', (b | (0x80 if number > 0 else 0)))

            if num == 0:
                break

        return out

    def unpack_varint(self, max_bits: int = 32) -> int:
        num = 0

        for i in range(10):
            b = struct.unpack(f'>B', self.read(1))
            num |= (b & 0x7F) << (7 * i)

            if not b & 0x80:
                break

        if num & (1 << 31):
            num -= 1 << 32

        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(f'num doesn\'t fit in given range: {num_min} <= {num} < {num_max}')

        return num

    def pack(self, comp_thresh: int = -1) -> bytes:
        if comp_thresh >= 0:
            if len(self.buf) >= comp_thresh:
                data = self.pack_varint(len(self.buf)) + zlib.compress(self.buf)
            else:
                data = self.pack_varint(0) + self.buf
        else:
            data = self.buf

        return self.pack_varint(len(data), max_bits=32) + data

    @classmethod
    def pack_string(cls, text: str) -> bytes:
        text = text.encode('utf-8')
        return self.pack_varint(len(text), max_bits=16) + text

    def unpack_string(self) -> str:
        length = self.unpack_varint(max_bits=16)
        return self.read(length).decode('utf-8')

    @classmethod
    def pack_json(cls, obj: object) -> bytes:
        return self.pack_string(json.dumps(obj))

    def unpack_json(self) -> object:
        return json.loads(self.unpack_string())
