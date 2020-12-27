from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp
import uuid

from src.types.packets.login.login import *
from src.types.buffer import Buffer

from src.util.encryption import *
from src.util.share import share

# https://github.com/ammaraskar/pyCraft/blob/master/minecraft/networking/encryption.py


async def request_encryption(r: 'StreamReader', w: 'StreamWriter', packet: 'LoginStart', lc: dict):
    packet = LoginEncryptionRequest(
        share['rsa']['public'].public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

    lc['verify'] = packet.verify_token

    w.write(Buffer.pack_packet(packet))
    await w.drain()


async def server_auth(packet: 'LoginEncryptionResponse', remote: tuple, cache: dict):
    if share['rsa']['private'].decrypt(packet.verify_token, PKCS1v15()) == cache['verify']:
        resp = await share['ses'].get(
            'https://sessionserver.mojang.com/session/minecraft/hasJoined',
            params={
                'username': cache['username'],
                'serverId': generate_verify_hash(
                    share['rsa']['private'].decrypt(packet.shared_key, PKCS1v15()),
                    share['rsa']['public'].public_bytes(
                        encoding=serialization.Encoding.DER,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )
            }
        )

        jj = await resp.json()

        if jj is not None:
            uuid_, name = uuid.UUID(jj['id']), jj['name']

            return uuid_, name

    return False


async def login_success(r: 'StreamReader', w: 'StreamWriter', username: str, uuid_: uuid.UUID = None):  # nopep8
    if uuid_ is None:
        resp = await share['ses'].get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        jj = await resp.json()
        uuid_ = uuid.UUID(jj['id'])

    w.write(Buffer.pack_packet(LoginSuccess(uuid_, username)))
    await w.drain()
