import Buffer from buffer
class Packet():
    """Base packet class used for networking stuff i don't get enough to explain here."""
    def __init__(self):
        self.length: int = 0
        self.id: int = 0
        self.data: list = []
