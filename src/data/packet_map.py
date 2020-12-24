import importlib
import os

__all__ = ('PACKET_MAP',)

PACKET_MAP = {}  # {state: (packet, packet,..),..}

for state in os.listdir('src/types/packets'):
    PACKET_MAP[state] = []

    for file in os.listdir(f'src/types/packets/{state}'):
        module_all = __import__(f'src.types.packets.{state}.{file}', fromlist=('__all__',))

        for name in module_all:
            PACKET_MAP[state] += __import__(f'src.types.packets.{state}.{file}', fromlist=module_all)

    PACKET_MAP[state] = tuple(sorted(PACKET_MAP[state], key=(lambda p: p.id)))
