import importlib
import os

__all__ = ('PACKET_MAP',)

PACKET_MAP = {}  # {state: (packet, packet,..),..}

def load_packets():
    for state in os.listdir('src.types.packets'):
        PACKET_MAP[state] = []

        for file in os.listdir(f'{path}/{state}'):
            module = importlib.import_module(file)

            for name in module.__all__:
                PACKET_MAP[state].append(module.__dict__.get(name))

        PACKET_MAP[state] = tuple(sorted(PACKET_MAP[state], key=(lambda p: p.id)))
