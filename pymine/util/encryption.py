from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.base import _CipherContext
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import asyncio

from pymine.types.stream import Stream

__all__ = ('gen_verify_hash', 'gen_aes_cipher', 'EncryptedStreamReader', 'EncryptedStreamWriter',)


def gen_rsa_keys():
    private_key = rsa.generate_private_key(65537, 1024)

    return private_key, private_key.public_key()


def gen_verify_hash(shared_key: bytes, public_key: bytes):
    verify_hash = hashlib.sha1()

    verify_hash.update((' ' * 20).encode('utf-8'))
    verify_hash.update(shared_key)
    verify_hash.update(public_key)

    return format(int.from_bytes(verify_hash.digest(), byteorder='big', signed=True), 'x')


def gen_aes_cipher(shared_key: bytes):
    return Cipher(algorithms.AES(shared_key), modes.CFB8(shared_key))


class EncryptedStream(Stream):
    def __init__(self, stream: Stream, decryptor: _CipherContext, encryptor: _CipherContext):
        super().__init__(stream.original_reader, stream.original_writer)

        self.decryptor = decryptor
        self.encryptor = encryptor

    async def read(self, n: int = -1):
        return self.decryptor.update(await self.stream.read(n))

    async def readline(self):
        return self.decryptor.update(await self.stream.readline())

    async def readexactly(self, n: int):
        return self.decryptor.update(await self.stream.readexactly(n))

    async def readuntil(self, separator=b'\n'):
        return self.decryptor.update(await self.stream.readuntil(separator))

    def write(self, data: bytes):
        return self.stream.write(self.encryptor.update(data))

    def writelines(self, data: bytes):
        return self.stream.writelines(self.encryptor.update(data))
