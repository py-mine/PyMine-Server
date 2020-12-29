from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import aiohttp
import uuid

from src.types.packets.login.set_comp import LoginSetCompression
from src.types.packets.login.login import *
from src.types.buffer import Buffer

from src.util.encryption import *
from src.util.share import share

login_cache = {}  # {remote: {username: username, verify_token: verify_token]}

states = share['states']


# Contains all the logic for logging in (handles all packets in the login state)
async def login(r: 'StreamReader', w: 'StreamWriter', packet: 'Packet', remote: tuple) -> tuple:
    if packet.id_ == 0x00:  # LoginStart
        if share['conf']['online_mode']:
            login_cache[remote] = {'username': packet.username, 'verify': None}
            await request_encryption(r, w, packet, login_cache[remote])
        else:  # If no auth is used, go straight to login success
            await login_success(r, w, packet.username)
    elif packet.id_ == 0x01:  # LoginEncryptionResponse
        shared_key, auth = await server_auth(packet, remote, login_cache[remote])

        del login_cache[remote]

        if not auth:
            await login_kick(w)
            return await share['close_con'](w, remote)

        # Generate a cipher for that client using the shared key from the client
        cipher = gen_aes_cipher(shared_key)

        # Replace streams with ones which auto decrypt + encrypt data when reading/writing
        r = EncryptedStreamReader(r, cipher.decryptor())
        w = EncryptedStreamWriter(w, cipher.encryptor())

        if share['comp_thresh'] > 0:  # Send set compression packet if needed
            await set_compression(w)

        await login_success(r, w, *auth)

        states[remote] = 3  # PLAY

    return True, r, w


# Send an encryption request packet to the client
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


# Verifies that the shared key and token are the same, and does other authentication methods
# Returns the decrypted shared key and the client's username and uuid
async def server_auth(packet: 'LoginEncryptionResponse', remote: tuple, cache: dict):
    if share['rsa']['private'].decrypt(packet.verify_token, PKCS1v15()) == cache['verify']:
        decrypted_shared_key = share['rsa']['private'].decrypt(packet.shared_key, PKCS1v15())

        resp = await share['ses'].get(
            'https://sessionserver.mojang.com/session/minecraft/hasJoined',
            params={
                'username': cache['username'],
                'serverId': gen_verify_hash(
                    decrypted_shared_key,
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

            return decrypted_shared_key, (name, uuid_,)

    return False, False


# Set the the compression threshold for all future packets
async def set_compression(w: 'StreamWriter'):
    w.write(Buffer.pack_packet(LoginSetCompression(share['comp_thresh'])))
    await w.drain()


# Tell the client they've logged in succesfully
async def login_success(r: 'StreamReader', w: 'StreamWriter', username: str, uuid_: uuid.UUID = None):  # nopep8
    if uuid_ is None:
        resp = await share['ses'].get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        jj = await resp.json()
        uuid_ = uuid.UUID(jj['id'])

    w.write(Buffer.pack_packet(LoginSuccess(uuid_, username), share['comp_thresh']))
    await w.drain()


# Tell the client they did a bad
async def login_kick(w: 'StreamWriter'):
    w.write(Buffer.pack_packet(
        LoginDisconnect('Failed to authenticate your connection.')
    ))
    await w.drain()
