from __future__ import annotations


class Packet:
    """Base Packet class.

    :param int id: Packet identifaction number. Defaults to -0x1.
    :attr id:
    """

    def __init__(self, id: int = -0x1) -> None:
        self.id = id
