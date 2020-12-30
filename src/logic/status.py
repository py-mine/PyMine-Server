from src.types.packets.handshaking.legacy_ping import HandshakeLegacyPingResponse
from src.types.packets.status.status import *
from src.types.buffer import Buffer

from src.util.share import share


# Handles all status logic (all packets in the status state)
async def status(r: 'StreamReader', w: 'StreamWriter', packet: 'Packet', remote: tuple) -> tuple:
    if packet.id_ == 0x00:  # StatusStatusRequest
        await send_status(r, w, packet)
    elif packet.id_ == 0x01:  # StatusStatusPingPong
        await pong(r, w, packet)
        return await share['close_con'](w, remote)

    return True, r, w


async def send_status(r: 'StreamReader', w: 'StreamWriter', packet: 'StatusStatusRequest') -> None:
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
                },
                {
                    'name': 'itsmewulf',
                    'id': '99fc4512-d91a-4ab5-bbce-f25e9a75bf21'
                }
            ]
        },
        'description': {  # a Chat
            'text': share['conf']['motd']
        }
    }

    if share['favicon'] is not None:
        data['favicon'] = share['favicon']

    w.write(Buffer.pack_packet(StatusStatusResponse(data)))
    await w.drain()


async def pong(r: 'StreamReader', w: 'StreamWriter', packet: 'StatusStatusPingPong') -> None:
    w.write(Buffer.pack_packet(packet))
    await w.drain()


async def legacy_ping(r: 'StreamReader', w: 'StreamWriter', remote: tuple) -> None:
    # while True:
    #     try:
    #         await asyncio.wait_for(r.read(1), 5)
    #     except BaseException:
    #         break

    w.write(Buffer.pack_packet(HandshakeLegacyPingResponse(
        share['version'],
        share['conf']['motd'],
        69,  # In the future should be the actual online players
        share['conf']['max_players']
    )))
