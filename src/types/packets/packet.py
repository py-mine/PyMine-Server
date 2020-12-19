import struct


class Packet:
    def __init__(self, format, ):
        self.buf = b''
        self.pos = 0
        self.format = None

    def add(self, data: bytes):
        self.buf += data

    def read(self, length: int = 1):
        try:
            return self.buf[self.pos:self.pos+length]
        finally:
            self.pos += length

    def reset(self):
        self.pos = 0

    def pack_array(f, array):
        self.buf += struct.pack(f'>{f*len(array)}', *array)

    def unpack_array(f, length):
        data = self.read(struct.calcsize(f'>{f}') * length)
        return list(struct.unpack(f'>{f*length}', data))

    def pack_bool(self, boolean):
        self.buf += struct.pack(f'>?', boolean)

    def unpack_bool(self):
        return struct.unpack(f'>?', self.read(1))
