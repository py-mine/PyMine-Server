from __future__ import annotations
import struct
import json
import zlib

from src.types.buffer import Buffer

class Packet(Buffer):
    """
    The base class for a packet, contains most
    necessary functions for dealing with the data
    in a packet that isn't covered by a Buffer
    """

    
