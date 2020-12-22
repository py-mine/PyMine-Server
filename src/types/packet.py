from buffer import Buffer 
class Packet(Buffer):
    """Base packet class used for networking stuff i don't get enough to explain here."""
    def __init__(self):
        self.length = 0
        self.id = 0
        self.data = []
