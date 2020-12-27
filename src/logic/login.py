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
    resp = await share['ses'].get(
        'https://sessionserver.mojang.com/session/minecraft/hasJoined?username=username&serverId=hash',
        params={
            'username': cache['username'],
            'serverId': generate_verify_hash(
                packet.shared_key,
                share['rsa']['public'].public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        }
    )

    jj = await resp.json()
    uuid_, name = uuid.UUID(jj['id']), jj['name']

    decrypted_verify = share['rsa']['private'].decrypt(packet.verify_token, PKCS1v15())
    if decrypted_verify == cache['verify']:
        print(True)


async def login_success(r: 'StreamReader', w: 'StreamWriter', username: str, uuid_: uuid.UUID = None):  # nopep8
    if uuid_ is None:
        resp = await share['ses'].get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        jj = await resp.json()
        uuid_ = uuid.UUID(jj['id'])

    w.write(Buffer.pack_packet(LoginSuccess(uuid_, username)))
    await w.drain()
