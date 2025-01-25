import itertools
import math
from copy import copy
from itertools import combinations
from multiprocessing import Pool
from typing import List, Tuple, Union

import numpy as np
from algebraic_immunity_utils.algebraic_immunity_utils import Matrix as GF2Matrix
from numpy.ma.extras import vander
from sage.all import *


def get_pivot(row):
    for idx, v in enumerate(row):
        if v == 1:
            return idx


def generalized_echelon_form_GF2(matrix):
    def get_pivot(row):
        for idx, val in enumerate(row):
            if val != 0:
                return idx
        return None

    def copy(matrix):
        return [row[:] for row in matrix]

    m_copy = copy(matrix)
    rows = len(m_copy)
    cols = len(m_copy[0])
    operations = []
    lead = 0

    for r in range(rows):
        if lead >= cols:
            break
        i = r
        while m_copy[i][lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if lead == cols:
                    return m_copy, operations
        m_copy[r], m_copy[i] = m_copy[i], m_copy[r]
        if r != i:
            operations.append((r, i))
            operations.append((i, i))
            operations.append((r, i))
        for i in range(rows):
            if i != r and m_copy[i][lead] == 1:
                m_copy[i] = [(x + y) % 2 for x, y in zip(m_copy[i], m_copy[r])]
                operations.append((i, r))
        lead += 1

    return m_copy, operations


def is_echelon_form(matrix):
    """
    Check if the given matrix is in echelon form.

    Args:
        matrix (list[list[float]]): 2D list representing the matrix.

    Returns:
        bool: True if the matrix is in echelon form, False otherwise.
    """
    # Number of rows and columns
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0

    last_leading_col = -1  # Track the last leading entry's column index

    for row in matrix:
        # Find the leading entry in the current row
        leading_col = next((i for i, val in enumerate(row) if val != 0), num_cols)

        # Check if the leading entry is strictly to the right of the last leading entry
        if leading_col <= last_leading_col and leading_col < num_cols:
            return False

        # Update the last leading column index
        last_leading_col = leading_col

        # Check if all entries below the leading entry are zeros
        leading_row_index = matrix.index(row)
        for i in range(leading_row_index + 1, num_rows):
            if matrix[i][leading_col] != 0:
                return False

    return True


class VMState:

    def __init__(self, vandermonde, z, z_c, e):
        self.vandermonde = vandermonde
        self.z = z
        self.z_c = z_c
        self.e = e
        self.operations = []


class IVRestrictedAI:

    def __init__(self, truth_table: List[int], n_vars: int = None):
        self.t_table = truth_table
        if n_vars is None:
            self.n = int(math.log(len(truth_table), 2))
        else:
            self.n = n_vars

    @staticmethod
    def str_exp(s1: str, s2: str) -> int:
        inter = [int(i) for i in s1]
        inter_e = [int(i) for i in s2]
        return math.prod([inter[i] ** inter_e[i] for i in range(len(inter))])

    @staticmethod
    def apply_operations(v: List[int], operations: List[Tuple[int, int]]) -> List[int]:
        for operation in operations:
            v[operation[0]] = (v[operation[0]] + v[operation[1]]) % 2
        return v

    @classmethod
    def compute_next(cls, v_previous: GF2Matrix, monom_slice: List[str], support_slice: List[str], idx: int,
                     operations: List[Tuple[int, int]]) -> GF2Matrix:
        row = [cls.str_exp(support_slice[-1], monom_slice[i]) for i in range(idx + 1)]
        column = [cls.str_exp(support_slice[i], monom_slice[-1]) for i in range(idx)]
        n_vect = cls.apply_operations(operations=operations, v=column)
        v_previous.append_column(n_vect)
        v_previous.append_row(row)
        return v_previous

    @classmethod
    def compute_v(cls, z: List[str], e: List[str]) -> GF2Matrix:
        return GF2Matrix([[cls.str_exp(z[i], e[j]) for j in range(len(e))] for i in range(len(z))])

    @staticmethod
    def is_submonomial(sub_monom: str, monom: str) -> bool:
        assert len(sub_monom) == len(monom)
        for char1, char2 in zip(sub_monom, monom):
            if char1 > char2:
                return False
        return True

    @classmethod
    def verify(cls, z: List[str], g: List[int], mapping: List[str]) -> Tuple[bool, Union[None, Tuple[int, str]]]:
        for idx, item in enumerate(z):
            anf = [g[i] for i in range(len(g)) if cls.is_submonomial(sub_monom=mapping[i], monom=item) is True]
            if sum(anf) % 2 == 1:
                return False, (idx, item)
        return True, None

    @classmethod
    def fill_matrix_will_all_s(cls, m: GF2Matrix, z, e_section) -> GF2Matrix:
        for i in range(len(z)):
            m.append_row([cls.str_exp(z[i], e_section[j]) for j in range(len(e_section))])
        return m

    @classmethod
    def append_column_operations(cls, m: GF2Matrix, z, e_i,
                                 operations) -> GF2Matrix:
        col = [cls.str_exp(z_i, e_i) for z_i in z]
        v = cls.apply_operations(v=col, operations=operations)
        m.append_column(v)
        return m

    @classmethod
    def append_column_operations2(cls, m: Matrix, z, e_i) -> GF2Matrix:
        colu = vector(GF(2),[cls.str_exp(z_i, e_i) for z_i in z])
        m = m.T.stack(colu).T
        # m = m.augment(colu)
        # m.append_column(col)
        return m

    @staticmethod
    def linear_combinations(base):
        # Get the dimension of the vectors (assumes all vectors have the same length)
        vector_length = len(base[0])

        # Generate all possible coefficients in GF(2) for the number of vectors in the base
        coefficients = itertools.product([0, 1], repeat=len(base))

        # combinations = []
        for coef_set in coefficients:
            if set(coef_set) == {0}:
                continue
            v = [
                sum(coeff * vec[i] for coeff, vec in zip(coef_set, base)) % 2
                for i in range(vector_length)
            ]
            yield v

            # combinations.append(v)


    @staticmethod
    def get_combinations(base):
        dim = len(base)

        # Filter out zero vectors
        non_zero_ker = base

        # for k in non_zero_ker:
        #     yield k
        to_ret = non_zero_ker

        # Generate all combinations of coefficients in {0, 1}
        l = list(itertools.product([0, 1], repeat=dim))
        for coeffs in l:
            # Compute the linear combination of the basis vectors
            # linear_combination = sum(coeff * np.array(vec) for coeff, vec in zip(coeffs, base))
            a = 1
            linear_combination = [
                sum(coeff * vec[i] for coeff, vec in zip(coeffs, non_zero_ker)) % 2
                for i in range(len(non_zero_ker[0]))
            ]

            # Skip zero vectors and vectors already in the kernel basis
            if linear_combination in non_zero_ker:
                continue
            # if sum(linear_combination.tolist()) == target_weight:
            to_ret.append(linear_combination)
            # yield linear_combination
        return to_ret

    def fin_min_annihilator_sequencial(self, z, z_c, e, s):
        vander_monde = GF2Matrix([[self.str_exp(z[0], e[0])]])
        vander_monde_c = GF2Matrix([[self.str_exp(z_c[0], e[0])]])

        states = [VMState(vandermonde=vander_monde, z=z, z_c=z_c, e=e),
                  VMState(vandermonde=vander_monde_c, z=z_c, z_c=z, e=e)]

        n_iters = min(len(z), len(z_c))
        i = 1
        idx = 0
        while i < n_iters:
            for state in states:
                vander_monde = IVRestrictedAI.compute_next(v_previous=state.vandermonde.copy(),
                                                           support_slice=state.z[:i + 1],
                                                           monom_slice=state.e[:i + 1], idx=i,
                                                           operations=state.operations)

                vandermonde, operations_i = vander_monde.row_echelon_full_matrix()
                #  assert is_echelon_form(vandermonde.to_list())
                # vandermonde, operations_i = echf_1(Matrix(GF(2), vander_monde.to_list()))
                # l_m = [[vandermonde[i][j] for j in range(vandermonde.ncols())] for i in range(vandermonde.nrows())]
                state.vandermonde = vandermonde
                if vandermonde.rank() < i + 1:
                    # m = Matrix(GF(2), vandermonde.to_list())
                    k = vandermonde.kernel()
                    # kl = [list(item) for item in k]
                    # k = vandermonde.kernel()
                    comb = IVRestrictedAI.linear_combinations(k)
                    for kv in comb:
                        # if np.any(kv[cutoff_position:]) is True:
                        #     breakpoint()
                        vanish_on_z, vanish_index = IVRestrictedAI.verify(z=state.z[i + 1:], mapping=state.e[:i + 1],
                                                                          g=kv)
                        if vanish_on_z is True:
                            # and state.e[i].count('1') == sum(kv)
                            vanish_on_s, _ = IVRestrictedAI.verify(z=state.z_c, g=kv, mapping=state.e[:i + 1])
                            if vanish_on_s is False:
                                return state.e[i].count('1')
                        # else:
                        #      new_index = i + vanish_index[0] + 1
                        #      state.z[i + 1], state.z[new_index] = state.z[new_index], state.z[i + 1]

                state.operations += operations_i
            i += 1
            idx += 1
        vander_monde_s = IVRestrictedAI.compute_v(z=s[:idx + 1], e=e[:idx + 1])
        vander_monde_s = IVRestrictedAI.fill_matrix_will_all_s(vander_monde_s.copy(), s[idx + 1:], e[:idx + 1])
        # vander_monde_s = Matrix(GF(2), vander_monde_s.to_list())
        vander_monde_s, operations_s = vander_monde_s.row_echelon_full_matrix()
        vandermonde = IVRestrictedAI.fill_matrix_will_all_s(states[0].vandermonde.copy(),
                                                                           states[0].z[idx + 1:],
                                                                           e[:idx + 1])
        # vandermonde, ops = generalized_echelon_form_GF2(vandermonde.to_list())
        vandermonde, ops = vandermonde.row_echelon_full_matrix()
        # states[0].vandermonde = GF2Matrix(vandermonde)
        states[0].vandermonde = vandermonde
        states[0].operations += ops
        vandermonde = IVRestrictedAI.fill_matrix_will_all_s(states[1].vandermonde.copy(),
                                                                           states[1].z[idx + 1:],
                                                                           e[:idx + 1])
        # vandermonde, ops = generalized_echelon_form_GF2(vandermonde.to_list())
        vandermonde, ops = vandermonde.row_echelon_full_matrix()
        # states[1].vandermonde = GF2Matrix(vandermonde)
        states[1].vandermonde = vandermonde
        states[1].operations += ops
        r_s = vander_monde_s.rank()

        # states[0].vandermonde = Matrix(GF(2), states[0].vandermonde.to_list)
        # states[1].vandermonde = Matrix(GF(2), states[1].vandermonde.to_list)

        if min([state.vandermonde.rank() for state in states]) < r_s:
            return e[idx].count('1')

        i = idx + 1
        s_len = len(s)
        while r_s <= math.ceil(s_len / 2):
            for state in states:
                vander_monde = IVRestrictedAI.append_column_operations(state.vandermonde.copy(), state.z, e[i],
                                                                       state.operations)
                vander_monde, ops = vander_monde.row_echelon_full_matrix()
                # vander_monde_s = IVRestrictedAI.append_column_operations2(vander_monde_s, s, e[i])
                vander_monde_s = IVRestrictedAI.append_column_operations(vander_monde_s.copy(), s, e[i], operations_s)
                vander_monde_s, ops_s = vander_monde_s.row_echelon_full_matrix()
                r_s = vander_monde_s.rank()
                # vander2 = Matrix(GF(2), vander_monde.to_list()).rank()
                # if vander2 != vander_monde.rank():
                 #    a = 1
                if vander_monde.rank() < r_s:
                    return e[i].count('1')
                state.vandermonde = vander_monde
                state.operations += ops
                operations_s += ops_s
            i += 1

    def find_min_annihilator(self, z: List[str], z_c: List[str], e: List[str], s: List[str]) -> Union[int, None]:
        vander_monde = GF2Matrix([[self.str_exp(z[0], e[0])]])
        idx = 0
        i = 1
        operations = []
        n_iters = len(z)

        while i < n_iters:
            vander_monde_old = vander_monde
            vander_monde = IVRestrictedAI.compute_next(v_previous=vander_monde.copy(), support_slice=z[:i + 1],
                                                       monom_slice=e[:i + 1], idx=i, operations=operations)
            vander_monde, operations_i = vander_monde.row_echelon_full_matrix()
            if vander_monde.rank() < i + 1:
                k = vander_monde.kernel()[0]
                vanish_on_z, vanish_index = IVRestrictedAI.verify(z=z[i + 1:], mapping=e[:i + 1], g=k)
                if vanish_on_z is True:
                    vanish_on_s, _ = IVRestrictedAI.verify(z=z_c, g=k, mapping=e[:i + 1])
                    if vanish_on_s is False:
                        return e[i].count('1')
                    else:
                        vander_monde = vander_monde_old
                        del e[i]
                        # e.remove(e[i])
                        continue
                else:
                    new_index = i + vanish_index[0] + 1
                    z[i + 1], z[new_index] = z[new_index], z[i + 1]

                    # tmp = z[i + 1]
                    # z[i + 1] = z[new_index]
                    # z[new_index] = tmp
            i += 1
            idx += 1
            operations += operations_i

        vander_monde_s = IVRestrictedAI.compute_v(z=s[:idx + 1], e=e[:idx + 1])
        vander_monde_s = IVRestrictedAI.fill_matrix_will_all_s(vander_monde_s.copy(), s[idx + 1:], e[:idx + 1])
        vander_monde_s, operations_s = vander_monde_s.row_echelon_full_matrix()
        r_s = vander_monde_s.rank()
        if vander_monde.rank() < r_s:
            return e[idx].count('1')

        i = idx + 1
        s_len = len(s)
        while r_s <= math.ceil(s_len / 2):
            vander_monde = IVRestrictedAI.append_column_operations(vander_monde, z, e[i], operations)
            vander_monde_s = IVRestrictedAI.append_column_operations(vander_monde_s, s, e[i], operations_s)
            r_s = vander_monde_s.rank()
            if vander_monde.rank() < r_s:
                return e[i].count('1')
            i += 1

    @staticmethod
    def generate_combinations(n, r):
        all_combinations = []
        for k in range(r + 1):
            for ones_positions in combinations(range(n), k):
                binary_string = ['0'] * n
                for pos in ones_positions:
                    binary_string[pos] = '1'
                all_combinations.append(''.join(binary_string))
        return [item[::-1] for item in all_combinations]

    @classmethod
    def compute_monomials(cls, n, r):
        combs = cls.generate_combinations(n=n, r=r)
        return combs

    def compute_z(self, s):
        true_idxs = []
        false_idxs = []
        s_bin = []
        for i in range(len(self.t_table)):
            if i not in s:
                continue
            if self.t_table[i] == 1:
                true_idxs.append(bin(i)[2:].zfill(self.n))
            else:
                false_idxs.append(bin(i)[2:].zfill(self.n))
            s_bin.append(bin(i)[2:].zfill(self.n))
        return true_idxs, false_idxs, s_bin

    def compute_z_for_dist(self, s):
        true_idxs = []
        false_idxs = []
        s_bin = []
        t_len = len(self.t_table)

        for i in range(t_len):
            if self.t_table[i] == 1:
                true_idxs.append(bin(s[i])[2:].zfill(self.n))
            else:
                false_idxs.append(bin(s[i])[2:].zfill(self.n))
            s_bin.append(bin(s[i])[2:].zfill(self.n))
        return true_idxs, false_idxs, s_bin

    @classmethod
    def algebraic_immunity(cls, truth_table: List[int], s: List[int], _hide=False, balance_ratio=1 / 4) -> int:
        f_ummu = IVRestrictedAI(truth_table=truth_table)
        z, z_c, s_bin = f_ummu.compute_z(s)
        if z == [] or z_c == []:
            return 0
        e = cls.compute_monomials(n=f_ummu.n, r=f_ummu.n)
        r = len(z) / len(z_c) if len(z) < len(z_c) else len(z_c) / len(z)
        # breakpoint()
        if r < balance_ratio:
            # if True:
            args = [
                (z, z_c, e, s_bin),
                (z_c, z, e, s_bin)
            ]
            # imm1 = f_ummu.find_min_annihilator(z, z_c, e, s_bin)

            # imm2 = f_ummu.find_min_annihilator(z_c, z, e, s_bin)

            # results = [imm1, imm2]
            with Pool(processes=2) as pool:
                results = pool.starmap(f_ummu.find_min_annihilator, args)
            return min([item for item in results if item is not None])
        else:
            return f_ummu.fin_min_annihilator_sequencial(z=z, z_c=z_c, e=e, s=s_bin)

    @classmethod
    def algebraic_immunity_dist(cls, s_image: List[int], s: List[int], n_vars: int, _verbose: bool = False,
                                _hide: bool = False) -> int:
        f_ummu = IVRestrictedAI(truth_table=s_image, n_vars=n_vars)

        z, z_c, s_bin = f_ummu.compute_z_for_dist(s)
        if z == [] or z_c == []:
            return 0
        e = cls.compute_monomials(n=f_ummu.n, r=f_ummu.n)
        args = [
            (z, z_c, e, s_bin),
            (z_c, z, e, s_bin)
        ]
        with Pool() as pool:
            results = pool.starmap(f_ummu.find_min_annihilator, args)
        return min([item for item in results if item is not None])
