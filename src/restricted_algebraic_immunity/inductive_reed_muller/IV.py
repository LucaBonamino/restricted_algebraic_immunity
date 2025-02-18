import itertools
import math
from itertools import combinations
from multiprocessing import Pool
from typing import List, Tuple, Union

from algebraic_immunity_utils import verify
from algebraic_immunity_utils.algebraic_immunity_utils import Matrix as GF2Matrix

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

    @staticmethod
    def linear_combinations(base: List[List[int]]) -> List[List[int]]:
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

    def fin_min_annihilator_sequencial(self, z, z_c, e, s) -> int:
        vander_monde = GF2Matrix([[self.str_exp(z[0], e[0])]])
        vander_monde_c = GF2Matrix([[self.str_exp(z_c[0], e[0])]])

        states = [VMState(vandermonde=vander_monde, z=z, z_c=z_c, e=e),
                  VMState(vandermonde=vander_monde_c, z=z_c, z_c=z, e=e)]

        n_iters = min(len(z), len(z_c))
        i = 1
        idx = 0
        while i < n_iters:
            for state in states:
                vander_monde = state.vandermonde.compute_next(
                    state.e[:i + 1],
                    state.z[:i + 1],
                    i,
                    state.operations
                )

                vandermonde, operations_i = vander_monde.row_echelon_full_matrix()
                state.vandermonde = vandermonde
                if vandermonde.rank() < i + 1:
                    k = vandermonde.kernel()
                    comb = IVRestrictedAI.linear_combinations(k)
                    for kv in comb:
                        vanish_on_z, vanish_index = verify(state.z[i + 1:], kv, state.e[:i + 1])
                        if vanish_on_z is True:
                            vanish_on_s, _ = verify(state.z_c, kv, state.e[:i + 1])
                            if vanish_on_s is False:
                                return state.e[i].count('1')
                        else:
                            new_index = i + vanish_index[0] + 1
                            state.z[i + 1], state.z[new_index] = state.z[new_index], state.z[i + 1]

                state.operations += operations_i
            i += 1
            idx += 1

        vander_monde_s = GF2Matrix(GF2Matrix.compute_vandermonde(s[:idx + 1], e[:idx + 1]))
        vander_monde_s = vander_monde_s.fill_rows(s[idx + 1:], e[:idx + 1])
        vander_monde_s, operations_s = vander_monde_s.row_echelon_full_matrix()
        vandermonde = states[0].vandermonde.fill_rows(states[0].z[idx + 1:], e[:idx + 1])

        vandermonde, ops = vandermonde.row_echelon_full_matrix()
        states[0].vandermonde = vandermonde
        states[0].operations += ops
        vandermonde = states[1].vandermonde.fill_rows(states[1].z[idx + 1:], e[:idx + 1])
        vandermonde, ops = vandermonde.row_echelon_full_matrix()
        states[1].vandermonde = vandermonde
        states[1].operations += ops
        r_s = vander_monde_s.rank()

        if min([state.vandermonde.rank() for state in states]) < r_s:
            return e[idx].count('1')

        i = idx + 1
        s_len = len(s)
        while r_s <= math.ceil(s_len / 2):
            for state in states:
                vander_monde = state.vandermonde.construct_and_add_column(state.z, e[i], state.operations)
                vander_monde, ops = vander_monde.row_echelon_full_matrix()
                vander_monde_s = vander_monde_s.construct_and_add_column(s, e[i], operations_s)
                vander_monde_s, ops_s = vander_monde_s.row_echelon_full_matrix()
                r_s = vander_monde_s.rank()
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
            vander_monde = vander_monde.compute_next(
                e[:i + 1],
                z[:i + 1],
                i,
                operations
            )
            vander_monde, operations_i = vander_monde.row_echelon_full_matrix()
            if vander_monde.rank() < i + 1:
                k = vander_monde.kernel()[0]
                vanish_on_z, vanish_index = verify(z[i + 1:], k, e[:i + 1])
                if vanish_on_z is True:
                    vanish_on_s, _ = verify(z_c, k, e[:i + 1])
                    if vanish_on_s is False:
                        return e[i].count('1')
                    else:
                        vander_monde = vander_monde_old
                        del e[i]
                        continue
                else:
                    new_index = i + vanish_index[0] + 1
                    z[i + 1], z[new_index] = z[new_index], z[i + 1]
            i += 1
            idx += 1
            operations += operations_i

        vander_monde_s = GF2Matrix(GF2Matrix.compute_vandermonde(s[:idx + 1], e[:idx + 1]))
        vander_monde_s = vander_monde_s.fill_rows(s[idx + 1:], e[:idx + 1])

        vander_monde_s, operations_s = vander_monde_s.row_echelon_full_matrix()
        r_s = vander_monde_s.rank()
        if vander_monde.rank() < r_s:
            return e[idx].count('1')

        i = idx + 1
        s_len = len(s)
        while r_s <= math.ceil(s_len / 2):
            vander_monde = vander_monde.construct_and_add_column(z, e[i], operations)
            vander_monde_s = vander_monde_s.construct_and_add_column(s, e[i], operations_s)
            vander_monde_2, ops_s = vander_monde_s.row_echelon_full_matrix()
            r_s = vander_monde_s.rank()
            if vander_monde.rank() < r_s:
                return e[i].count('1')
            i += 1
            operations_s += ops_s

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
        if r >= balance_ratio:
            args = [
                (z, z_c, e, s_bin),
                (z_c, z, e, s_bin)
            ]
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
        with Pool(processes=2) as pool:
            results = pool.starmap(f_ummu.find_min_annihilator, args)
        return min([item for item in results if item is not None])
