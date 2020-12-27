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
                    'name': 'Iapetus11',
                    'id': 'cbcfa252-867d-4bda-a214-776c881cf370'
                },
                {
                    'name': 'Sh_wayz',
                    'id': 'cbcfa252-867d-4bda-a214-776c881cf370'
                },
                {
                    'name': 'itsmewulf',
                    'id': '99fc4512-d91a-4ab5-bbce-f25e9a75bf21'
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
