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

def main(args):
    generators = make_generator_vectors(args)
    vertices = generate_vertices(generators)
    vertex_indices = number_vertices(vertices)
    vertex_list = make_vertex_list(vertices)
    print(vertex_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vector_count", type=int, help="number of initial vectors n. The polar zonohedron will have n-fold symmetry.")
    parser.add_argument("pitch_angle_degrees", type=float, help="pitch of the initial vectors in degrees. near 0 makes a pancake, near 90 produces a cigar shape")
    args = parser.parse_args()
    main(args)