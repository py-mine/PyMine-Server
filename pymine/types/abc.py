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


class AbstractPlugin:
    """Used to create plugin cogs."""


class AbstractWorldGenerator:
    """Abstract class used to create a world generator."""

    @classmethod
    def generate_chunk(cls, seed: int, dimension: str, chunk_x: int, chunk_z: int):  # -> Chunk
        raise NotImplementedError(cls.__name__)


class AbstractChunkIO:
    """Abstract class used to create chunk io."""

    @classmethod
    def calc_offset(cls, chunk_x: int, chunk_z: int) -> int:
        raise NotImplementedError(cls.__name__)

    @classmethod
    def find_chunk(cls, location: int) -> tuple:
        raise NotImplementedError(cls.__name__)

    @classmethod
    def fetch_chunk(cls, world_path: str, chunk_x: int, chunk_z: int):  # -> Chunk
        raise NotImplementedError(cls.__name__)

    @classmethod
    async def fetch_chunk_async(cls, world_path: str, chunk_x: int, chunk_z: int):  # -> Chunk
        raise NotImplementedError(cls.__name__)


class AbstractParser:
    """Abstract class used to create command argument parsers."""

    @classmethod
    def parse(cls, s: str) -> tuple:  # should return the chars used and data
        raise NotImplementedError(cls.__name__)


class AbstractPalette:
    """Abstract class used to distinguish whether a class is a block palette or not."""

    @classmethod
    def get_bits_per_block(cls):
        raise NotImplementedError(cls.__name__)

    @classmethod
    def encode(cls):
        raise NotImplementedError(cls.__name__)

    @classmethod
    def decode(cls):
        raise NotImplementedError(cls.__name__)


class AbstractEvent:
    """Used to create event classes for event handling."""

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)
