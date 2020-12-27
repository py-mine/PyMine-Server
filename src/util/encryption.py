from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib

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
