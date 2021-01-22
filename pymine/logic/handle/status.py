from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.stream import Stream

import pymine.types.packets.status.status as status_packets

from pymine.server import server


@server.api.events.on_packet("status", 0x00)
async def send_status(stream: Stream, packet: Packet) -> tuple:
    data = {
        "version": {"name": server.meta.version, "protocol": server.meta.protocol},
        "players": {
            "max": server.conf['max_players'],
            "online": len(server.cache.states),
            "sample": [
                {"name": "Iapetus11", "id": "cbcfa252-867d-4bda-a214-776c881cf370"},
                {"name": "Sh_wayz", "id": "cbcfa252-867d-4bda-a214-776c881cf370"},
                {"name": "emeralddragonmc", "id": "eb86dc19-c3f5-4aef-a50e-a4bf435a7528"},
            ],
        },
        "description": {"text": server.conf["motd"]},  # a Chat
    }

    if server.favicon:
        data['favicon'] = server.favicon

    stream.write(Buffer.pack_packet(status_packets.StatusStatusResponse(data)))
    await stream.drain()

    return True, stream


@server.api.events.on_packet("status", 0x01)
async def send_pong(stream: Stream, packet: Packet) -> tuple:
    stream.write(Buffer.pack_packet(packet))
    await stream.drain()

    return False, stream
