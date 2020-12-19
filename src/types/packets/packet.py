import struct


class Packet:
    def __init__(self, format, ):
        self.buf = b''
        self.pos = 0
        self.format = None

    def add(self, data: bytes):
        self.buf += data

    def read(self, length: int = 1) -> bytes:
        try:
            return self.buf[self.pos:self.pos+length]
        finally:
            self.pos += length

    def reset(self) -> None:
        self.pos = 0

    def pack_array(f, array: list) -> None:
        self.buf += struct.pack(f'>{f*len(array)}', *array)

    def unpack_array(f, length: int) -> list:
        data = self.read(struct.calcsize(f'>{f}') * length)
        return list(struct.unpack(f'>{f*length}', data))

    def pack_bool(self, boolean) -> None:
        self.buf += struct.pack(f'>?', boolean)

    def unpack_bool(self) -> bool:
        return struct.unpack(f'>?', self.read(1))

    def pack_varint(self, num: int, max_bits: int = 32) -> None:
        num_min, num_max = (-1 << (max_bits - 1)), (+1 << (max_bits - 1))

        if not (num_min <= num < num_max):
            raise ValueError(f'num doesn\'t fit in given range: {num_min} <= {num} < {num_max}')

        if num < 0:
            num += 1 + 1 << 32

        for i in range(10):
            b = num & 0x7F
            num >>= 7

            self.buf += struct.pack('>B', (b | (0x80 if number > 0 else 0)))

            if num == 0:
                break

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
