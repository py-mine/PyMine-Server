import importlib
import os

from src.util.immutable import make_immutable

__all__ = ('PACKET_MAP',)

PACKET_MAP = {}  # {state: (packet, packet,..),..}


def load_packets():
    for state in os.listdir('src/types/packets'):
        PACKET_MAP[state] = []

        for file in os.listdir(f'src/types/packets/{state}'):
            if file.endswith('.py'):
                module = importlib.import_module(f'src.types.packets.{state}.{file[:-3]}')

                for name in module.__all__:
                    PACKET_MAP[state].append(module.__dict__.get(name))

        PACKET_MAP[state] = sorted(PACKET_MAP[state], key=(lambda p: p.id_))

    PACKET_MAP = make_immutable(PACKET_MAP)


load_packets()
