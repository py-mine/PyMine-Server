import importlib
import os

from pymine.util.immutable import make_immutable

__all__ = (
    "PACKET_MAP",
    "PACKET_MAP_CLIENTBOUND",
)


def load_packets():
    packet_map = {}
    packet_map_clientbound = {}

    for state in os.listdir("pymine/types/packets"):
        packet_map[state] = {}
        packet_map_clientbound[state] = {}

        for file in filter((lambda f: f.endswith(".py")), os.listdir(f"pymine/types/packets/{state}")):
            module = importlib.import_module(f"pymine.types.packets.{state}.{file[:-3]}")

            for name in module.__all__:
                packet = module.__dict__.get(name)
                if packet.to == 2:
                    packet_map[state][packet.id] = packet_map_clientbound[state][packet.id] = packet
                elif packet.to == 1:
                    packet_map_clientbound[state][packet.id] = packet
                elif packet.to == 0:
                    packet_map[state][packet.id] = packet
                else:
                    raise ValueError(f"The direction of packet {type(packet).__name__} is invalid.")

    return make_immutable(packet_map), make_immutable(packet_map_clientbound)


PACKET_MAP, PACKET_MAP_CLIENTBOUND = load_packets()
