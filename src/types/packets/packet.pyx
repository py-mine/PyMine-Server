
cdef class Packet:
    cdef bytes buf
    cdef int pos

    def __init__(self):
        self.buf = b''
        self.pos = 0

    cdef def add(self, bytes data):
        self.buf += data

    def read(self, int data):
        pass
