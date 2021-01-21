from pymine.util.share import share, logger
from pymine.api.packet import handle_packet

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.stream import Stream

import pymine.types.packets.status.status as status_packets


@handle_packet("status", 0x00)
async def send_status(stream: Stream, packet: Packet) -> tuple:
    data = {
        "version": {"name": share["version"], "protocol": share["protocol"]},
        "players": {
            "max": share["conf"]["max_players"],
            "online": len(share["states"]),
            "sample": [
                {"name": "Iapetus11", "id": "cbcfa252-867d-4bda-a214-776c881cf370"},
                {"name": "Sh_wayz", "id": "cbcfa252-867d-4bda-a214-776c881cf370"},
                {"name": "emeralddragonmc", "id": "eb86dc19-c3f5-4aef-a50e-a4bf435a7528"},
            ],
        },
        "description": {"text": share["conf"]["motd"]},  # a Chat
    }

    if share["favicon"]:
        data["favicon"] = share["favicon"]

    stream.write(Buffer.pack_packet(status_packets.StatusStatusResponse(data)))
    await stream.drain()

    return True, stream


@handle_packet("status", 0x01)
async def send_pong(stream: Stream, packet: Packet) -> tuple:
    stream.write(Buffer.pack_packet(packet))
    await stream.drain()

    return False, stream
