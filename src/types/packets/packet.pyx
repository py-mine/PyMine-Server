
cdef class Packet:
    cdef bytes buf
    cdef int pos

    def __init__(self):
        self.buf = b''
        self.pos = 0

    cdef add(self, bytes data):
        self.buf += data

    cdef read(self, int data):
        pass
