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
