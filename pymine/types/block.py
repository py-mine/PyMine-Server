import ctypes


class BlockState(ctypes.Structure):
    _fields_ = [("block_id", ctypes.c_wchar_p), ("state", ctypes.c_byte)]
