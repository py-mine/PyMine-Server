import numpy

from pymine.util.misc import remove_namespace
from pymine.types.abc import AbstractPalette
from pymine.types.chunk import Chunk


def dump_to_obj(file, pymine_chunk: Chunk, palette: AbstractPalette):
    chunk = numpy.ndarray((256, 16, 16), numpy.uint64)
    chunk.fill(0)

    for section in pymine_chunk.sections.values():
        if section.y >= 0:
            chunk[section.y : section.y + 16] = section.block_states

    air = palette.encode("minecraft:air")

    points = {}
    rpoints = {}
    faces = {}
    rfaces = {}

    def append_point(*p) -> None:
        if not rpoints.get(p):
            points[len(points) - 1] = p
            rpoints[p] = len(points) - 1

    def append_face(f) -> None:
        if not rfaces.get(f):
            faces[len(faces) - 1] = f
            rfaces[f] = len(faces) - 1

    for y in range(256):
        for z in range(16):
            for x in range(16):
                if chunk[y, z, x] == air:
                    continue

                append_point(x, y, z)
                append_point(x + 1, y, z)
                append_point(x, y + 1, z)
                append_point(x, y, z + 1)
                append_point(x + 1, y + 1, z)
                append_point(x, y + 1, z + 1)
                append_point(x + 1, y, z + 1)
                append_point(x + 1, y + 1, z + 1)

    for y in range(256):
        for z in range(16):
            for x in range(16):
                block = chunk[y, z, x]

                if block == air:
                    continue

                block = remove_namespace(palette.decode(block)["name"])

                i1 = rpoints.get((x, y, z)) + 1
                i2 = rpoints.get((x + 1, y, z)) + 1
                i3 = rpoints.get((x, y + 1, z)) + 1
                i4 = rpoints.get((x, y, z + 1)) + 1
                i5 = rpoints.get((x + 1, y + 1, z)) + 1
                i6 = rpoints.get((x, y + 1, z + 1)) + 1
                i7 = rpoints.get((x + 1, y, z + 1)) + 1
                i8 = rpoints.get((x + 1, y + 1, z + 1)) + 1

                append_face(f"usemtl {block}\nf {i1} {i2} {i7} {i4}")
                append_face(f"usemtl {block}\nf {i1} {i2} {i5} {i3}")
                append_face(f"usemtl {block}\nf {i4} {i7} {i8} {i6}")
                append_face(f"usemtl {block}\nf {i1} {i4} {i6} {i3}")
                append_face(f"usemtl {block}\nf {i2} {i5} {i8} {i7}")
                append_face(f"usemtl {block}\nf {i3} {i5} {i8} {i6}")

    file.write("\n".join([f"v {p[0]} {p[1]} {p[2]}" for p in points.values()]) + "\n" + "\n".join(faces.values()))
