from pymine.types.chunk import Chunk


class AbstractWorldGenerator:
    """Abstract class used to create a world generator."""

    @staticmethod
    def generate_chunk(seed: int, chunk_x: int, chunk_z: int) -> Chunk:
        raise NotImplementedError(self.__class__.__name__)
