
from pymine.types.Region import Region
from pymine.types.chunk import Chunk

from pymine.api.world_gen import AbstractWorldGenerator


class SuperFlatWorldGenerator(AbstractWorldGenerator):
    def generate_chunk(self, chunk_x: int, chunk_z: int) -> Chunk:
        pass

    def generate_region(self, region_x: int, region_z: int) -> Region:
        raise NotImplementedError(self.__class__.__name__)
