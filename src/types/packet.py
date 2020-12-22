from buffer import Buffer

class Packet(Buffer):
    """Base packet class."""

    def __init__(self):
        self.length = 0
        self.id = 0
        self.data = []
