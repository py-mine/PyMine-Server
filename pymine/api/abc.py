from pymine.types.region import Region
from pymine.types.chunk import Chunk


class AbstractWorldGenerator:
    """Abstract class used to create a world generator.

    :param int seed: The seed used to generate the world.
    :ivar seed:
    """

    def __init__(self, seed: int) -> None:
        self.seed = seed

    def generate_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        raise NotImplementedError(self.__class__.__name__)

    def generate_region(self, region_x: int, region_z: int) -> Region:
        raise NotImplementedError(self.__class__.__name__)
