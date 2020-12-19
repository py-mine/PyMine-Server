
class Packet:
    def __init__(self):
        self.buf = b''
        self.pos = 0

    def add(self, data: bytes):
        self.buf += data

    def read(self, data: int):
        pass
