import numpy as np
import struct

def load_large_bit_matrix_bin(filename):
    with open(filename, "rb") as f:
        # Read dimensions (2 unsigned 32-bit integers)
        rows, cols = struct.unpack("<II", f.read(8))  # "<II" = little-endian, 2 uint32

        # Read the rest of the file as a flat array of 32-bit integers
        flat_array = np.frombuffer(f.read(), dtype=np.int32)

        # Reshape into the original matrix
        matrix = flat_array.reshape(rows, cols)

    return matrix