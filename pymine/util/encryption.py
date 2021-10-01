# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import asyncio

__all__ = (
    "gen_rsa_keys",
    "gen_verify_hash",
    "gen_aes_cipher",
)


def gen_rsa_keys():
    private_key = rsa.generate_private_key(
        65537, 1024
    )  # nosec : expected by the client, only used for negotiation

    return private_key, private_key.public_key()


def gen_verify_hash(shared_key: bytes, public_key: bytes):
    verify_hash = hashlib.sha1()  # nosec : shared client verification only

    verify_hash.update((" " * 20).encode("utf-8"))
    verify_hash.update(shared_key)
    verify_hash.update(public_key)

    return format(int.from_bytes(verify_hash.digest(), byteorder="big", signed=True), "x")


def gen_aes_cipher(
    shared_key: bytes,
):  # cipher used to encrypt + decrypt data sent via an encrypted socket
    return Cipher(algorithms.AES(shared_key), modes.CFB8(shared_key))
