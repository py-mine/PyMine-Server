
from src.types.packets.status.status import *
from src.types.buffer import Buffer


async def status(r, w, packet):
    global share

    data = {
        'version': {
            'name': share['version'],
            'protocol': packet.protocol
        },
        'players': {
            'max': share['PROPERTIES']['max-players'],
            'online': len(share['states']),
            'sample': [
                {
                    'name': 'thinkofdeath',
                    'id': '4566e69f-c907-48ee-8d71-d7ba5aa00d20'
                }
            ]
        },
        'description': {  # a Chat
            'text': share['PROPERTIES']['motd']
        },
        'favicon': share['favicon']
    }

    w.write(Buffer.pack_packet(StatusStatusResponse(data)))
