from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from asyncio import StreamReader, StreamWriter
import aiohttp
import uuid

from src.api import handle_packet

from src.util.encryption import *
from src.util.share import share

from src.types.packet import Packet

from src.types.packets.login.set_comp import LoginSetCompression
from src.types.packets.login.login import *

login_cache = {}
states = share['states']


@handle_packet('login', 0x00)
async def login_start(r: 'StreamReader', w: 'StreamWriter', packet: Packet, remote: tuple) -> tuple:
    if share['conf']['online_mode']:  # Online mode is enabled, so we request encryption
        lc = login_cache[remote] = {'username': packet.username, 'verify': None}

        packet = LoginEncryptionRequest(
            share['rsa']['public'].public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

        lc['verify'] = packet.verify_token

        w.write(Buffer.pack_packet(packet))
        await w.drain()
    else:  # No need for encryption since online mode is off, just send login success
        uuid_ = uuid.uuid4()  # This should be only generated if the player name isn't found in the world data, but no way to do that rn

        w.write(Buffer.pack_packet(LoginSuccess(uuid_, packet.username), share['comp_thresh']))
        await w.drain()

        states[remote] = 3  # Update state to play
