from asyncio import StreamReader, StreamWriter

from src.util.share import share, logger
from src.api import handle_packet

from src.types.packet import Packet
from src.types.buffer import Buffer

from src.types.packets.status.status import *


@handle_packet('status', 0x00)
async def send_status(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    data = {
        'version': {
            'name': share['version'],
            'protocol': share['protocol']
        },
        'players': {
            'max': share['conf']['max_players'],
            'online': len(share['states']),
            'sample': [
                {
                    'name': 'Iapetus11',
                    'id': 'cbcfa252-867d-4bda-a214-776c881cf370'
                },
                {
                    'name': 'Sh_wayz',
                    'id': 'cbcfa252-867d-4bda-a214-776c881cf370'
                }
            ]
        },
        'description': {  # a Chat
            'text': share['conf']['motd']
        },
        'favicon': share['favicon']
    }

    w.write(Buffer.pack_packet(StatusStatusResponse(data)))
    await w.drain()

    return True, r, w


@handle_packet('status', 0x01)
async def send_pong(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    w.write(Buffer.pack_packet(packet))
    await w.drain()

    return False, r, w
