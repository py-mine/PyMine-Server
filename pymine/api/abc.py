import aiofile

from pymine.types.chunk import Chunk


class AbstractWorldGenerator:
    """Abstract class used to create a world generator."""

    @staticmethod
    def generate_chunk(seed: int, chunk_x: int, chunk_z: int) -> Chunk:
        raise NotImplementedError(self.__class__.__name__)


class AbstractChunkIO:
    """Abstract class used to create chunk io."""

    @staticmethod
    async def fetch_chunk(path: str, chunk_x: int, chunk_z: int) -> Chunk:
        raise NotImplementedError(self.__class__.__name__)
