from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.base import _CipherContext
import hashlib
import asyncio

__all__ = ('gen_verify_hash', 'gen_aes_cipher',)


def gen_verify_hash(shared_key: bytes, public_key: bytes):
    verify_hash = hashlib.sha1()

    verify_hash.update((' ' * 20).encode('utf-8'))
    verify_hash.update(shared_key)
    verify_hash.update(public_key)

    return format(int.from_bytes(verify_hash.digest(), byteorder='big', signed=True), 'x')


def gen_aes_cipher(shared_key: bytes):
    return Cipher(
        algorithms.AES(shared_key),
        modes.CFB8(shared_key)
    )


class EncryptedStreamReader:  # Used to encrypt data read via a StreamReader
    def __init__(self, reader: asyncio.StreamReader, decryptor: '_CipherContext'):
        self.reader = reader
        self.decryptor = decryptor

    async def read(self, n: int = -1):
        return self.decryptor.update(await self.reader.read(n))


class EncryptedStreamWriter:  # Used to encrypt data sent via a StreamWriter
    def __init__(self, writer: asyncio.StreamWriter, encryptor: '_CipherContext'):
        self.writer = writer
        self.encryptor = encryptor

    def write(self, data: bytes):
        return self.writer.write(self.encryptor.update(data))

    def close(self):
        return self.writer.close()

    def get_extra_info(self, name: str, default: object = None):
        return self.writer.get_extra_info(name, default)

    async def drain(self):
        return await self.writer.drain()

    async def wait_closed(self):
        return await self.writer.wait_closed()
