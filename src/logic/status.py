#from src.types.packets.handshaking.legacy_ping import *
from src.types.packets.status.status import *
from src.types.buffer import Buffer

from src.util.share import share


async def status(r: 'StreamReader', w: 'StreamWriter', packet: 'StatusStatusRequest'):
    data = {
        'version': {
            'name': share['version'],
            'protocol': share['protocol']
        },
        'players': {
            'max': share['properties']['max_players'],
            'online': len(share['states']),
            'sample': [
                {
                    'name': 'thinkofdeath',
                    'id': '4566e69f-c907-48ee-8d71-d7ba5aa00d20'
                }
            ]
        },
        'description': {  # a Chat
            'text': share['properties']['motd']
        }
    }

    if share['favicon'] is not None:
        data['favicon'] = share['favicon']

    w.write(Buffer.pack_packet(StatusStatusResponse(data)))
    await w.drain()


async def pong(r: 'StreamReader', w: 'StreamWriter', packet: 'StatusStatusPingPong'):
    w.write(Buffer.pack_packet(packet))
    await w.drain()
