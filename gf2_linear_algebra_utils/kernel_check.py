from sage.all import *

def kernel_of_non_reduced_echelon_GF2(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_positions = []
    free_vars = []

    # Identify pivot positions and free variables
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                pivot_positions.append(j)
                break

    free_vars = [j for j in range(cols) if j not in pivot_positions]

    # Create basis vectors for the kernel
    kernel_basis = []

    for free_var in free_vars:
        basis_vector = [0] * cols
        basis_vector[free_var] = 1

        for row in range(rows):
            pivot_col = pivot_positions[row] if row < len(pivot_positions) else None
            if pivot_col is not None and matrix[row][free_var] == 1:
                basis_vector[pivot_col] = 1

        kernel_basis.append(basis_vector)

    return kernel_basis

# Example usage
M = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

kernel_basis = kernel_of_non_reduced_echelon_GF2(M)

import numpy as np
M_np = np.array(M)
print("Matrix M:")
print(M_np)

print("Kernel Basis:")
for vector in kernel_basis:
    print(np.array(vector))

# Verify by multiplying M and each vector in the kernel_basis
print("Verification (M * kernel_basis):")
for vector in kernel_basis:
    result = np.dot(M_np, vector) % 2
    print(result)


M_sage = Matrix(GF(2), M)


