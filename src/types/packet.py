from __future__ import annotations


class Packet:
    """Base Packet class.

    :param int id: Packet identifaction number. Defaults to -0x1.
    :param int comp_thresh: Compression threshold. Defaults to -1 (no compression).
    :attr id:
    :attr comp_thresh:
    """

    def __init__(self, id: int = -0x1, comp_thresh: int = -1) -> None:
        self.id = id
        self.comp_thresh = comp_thresh
