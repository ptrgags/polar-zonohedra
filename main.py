"""
Script to generate a polar zonohedra, as explained in the 2021 Bridges math art
paper "The Joy of Polar Zonohedra" by George Hart

http://archive.bridgesmathart.org/2021/bridges2021-7.pdf
"""

import argparse

import numpy
import pymesh

def make_generator_vectors(args):
    pitch_angle = args.pitch_angle_degrees * numpy.pi / 180.0
    z = numpy.sin(pitch_angle)
    s = numpy.cos(pitch_angle)
    n = args.vector_count
    generators = numpy.zeros((n, 3), dtype=numpy.float64)
    for i in range(n):
        angle = i / n * 2.0 * numpy.pi
        generators[i, 0] = s * numpy.cos(angle)
        generators[i, 1] = s * numpy.sin(angle)
        generators[i, 2] = z
    return generators

def cyclic_sum(generators, start, end):
    n = len(generators)
    result = numpy.zeros(3)
    for i in range(start, end + 1):
        result += generators[i % n]
    return result

def generate_vertices(generators):
    n = len(generators)
    # first and last rows are for the two points. Every other row
    # is a ring of n vertices.
    result = numpy.zeros((n + 1, n, 3), dtype=numpy.float64)

    # the first vertex is always the origin
    result[0, 0] = [0, 0, 0]

    # the middle n-1 layers are sums of i of the generator vectors. Indices
    # are treated cyclically
    for i in range(n - 1):
        for j in range(n):
            result[i, j] = cyclic_sum(generators, j, j + i)

    # the final vertex is the sum of all the generator vectors
    result[-1, 0] = numpy.sum(generators, axis=0)
    return result

def number_vertices(vertices):
    rows, columns, _ = vertices.shape
    indices = numpy.zeros((rows, columns), dtype=numpy.uint16)
    indices[0, 0] = 0

    next_index = 1
    for i in range(1, rows - 1):
        for j in range(columns):
            indices[i, j] = next_index
            next_index += 1
        
    indices[-1, 0] = next_index
    return indices

def make_vertex_list(vertices):
    rows, columns, _ = vertices.shape
    total_vertices = (rows - 2) * columns + 2
    vertex_list = numpy.zeros((total_vertices, 3), dtype=numpy.float64)

    vertex_list[0] = vertices[0, 0]

    next_index = 1
    for i in range(1, rows - 1):
        for j in range(columns):
            vertex_list[next_index] = vertices[i, j]
            next_index += 1

    vertex_list[-1] = vertices[-1, 0]
    return vertex_list

def make_face_list(indices):
    _, columns = indices.shape
    rhomb_count = columns * (columns - 1)
    triangle_count = rhomb_count * 2
    triangles_per_row = columns * 2
    face_list = numpy.zeros((triangle_count, 3), dtype=numpy.uint16)

    # the first row of faces shares the bottom point
    bottom_point = indices[0, 0]
    for j in range(columns):
        # two middle vertices of the rhombus
        v1 = indices[1, j]
        v2 = indices[1, (j + 1) % columns]
        # furthest point on the rhombus
        v3 = indices[2, j]
        # describe the rhombus as two triangles
        #
        #  bottom_point
        #     /  \
        #   v1----v2
        #     \  /
        #      v3
        face_list[2 * j] = [bottom_point, v1, v2]
        face_list[2 * j + 1] = [v3, v2, v1]

    for i in range(1, columns - 1):
        row_offset = i * triangles_per_row
        for j in range(columns):
            next_column = (j + 1) % columns
            v1 = indices[i, next_column]
            v2 = indices[i + 1, j]
            v3 = indices[i + 1, next_column]
            v4 = indices[i + 2, j]

            #
            #      v1
            #     /  \
            #   v2----v3
            #     \  /
            #      v4
            face_list[row_offset + 2 * j] = [v1, v2, v3]
            face_list[row_offset + 2 * j + 1] = [v4, v3, v2]

    # the last row of faces is similar to the first row, but the
    # shared vertex is on the other end
    top_point = indices[-1, 0]
    row_offset = (columns - 2) * triangles_per_row
    for j in range(columns):
        next_column = (j + 1) % columns
        v1 = indices[-3, next_column]
        v2 = indices[-2, j]
        v3 = indices[-2, next_column]

        # rhombus looks like this:
        #
        #      v1
        #     /  \
        #   v2----v3
        #     \  /
        #   top_point
        face_list[row_offset + 2 * j] = [v1, v2, v3]
        face_list[row_offset + 2 * j + 1] = [top_point, v3, v2]
    
    return face_list

def main(args):
    generators = make_generator_vectors(args)
    vertices = generate_vertices(generators)
    vertex_indices = number_vertices(vertices)
    vertex_list = make_vertex_list(vertices)
    face_list = make_face_list(vertex_indices)
    print(vertex_indices)
    print(face_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vector_count", type=int, help="number of initial vectors n. The polar zonohedron will have n-fold symmetry.")
    parser.add_argument("pitch_angle_degrees", type=float, help="pitch of the initial vectors in degrees. near 0 makes a pancake, near 90 produces a cigar shape")
    args = parser.parse_args()
    main(args)