import numpy as np
import struct

from algebraic_immunity_utils import Matrix
from sage.all import *


def load_large_bit_matrix_bin(filename):
    with open(filename, "rb") as f:
        # Read dimensions (2 unsigned 32-bit integers)
        rows, cols = struct.unpack("<II", f.read(8))  # "<II" = little-endian, 2 uint32

        # Read the rest of the file as a flat array of 32-bit integers
        flat_array = np.frombuffer(f.read(), dtype=np.int32)

        # Reshape into the original matrix
        matrix = flat_array.reshape(rows, cols)

    return matrix


n = 16
# Example usage
# matrix = load_large_bit_matrix_bin(f"large_bit_matrix_{n}.bin")
#print(matrix)


# M = Matrix(GF(2), matrix.tolist())
# G = codes.BinaryReedMullerCode(n, n).generator_matrix()
# # assert M == G
# print(M.ncols())
# print(G.ncols())
#
# for i in range(M.nrows()):
#     assert len(M[i]) == len(G[i])
#     if M[i] != G[i]:
#         print(i)
#         print(G[i])
#         print(M[i])
#
# assert G == M

import random
Matrix(GF(2), 2**16, 2**16, [random.randint(0, 1) for _ in range(2**16 * 2**16)])

