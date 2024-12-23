import math
from itertools import combinations
from multiprocessing import Pool
from typing import List, Tuple, Union

from algebraic_immunity_utils.algebraic_immunity_utils import Matrix as GF2Matrix


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
    def verify(cls, z:List[str], g: List[int], mapping: List[str]) -> Tuple[bool, Union[None, Tuple[int, str]]]:
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
            vander_monde, operations_i = vander_monde.echelon_form_last_row()
            if vander_monde.rank() < i + 1:
                k = vander_monde.kernel()[0]
                vanish_on_z, vanish_index = IVRestrictedAI.verify(z=z[i + 1:], mapping=e[:i + 1], g=k)
                if vanish_on_z is True:
                    vanish_on_s, _ = IVRestrictedAI.verify(z=z_c, g=k, mapping=e[:i + 1])
                    if vanish_on_s is False:
                        return e[i].count('1')
                    else:
                        vander_monde = vander_monde_old
                        e.remove(e[i])
                        continue
                else:
                    new_index = i + vanish_index[0] + 1
                    tmp = z[i + 1]
                    z[i + 1] = z[new_index]
                    z[new_index] = tmp
            i += 1
            idx += 1
            operations += operations_i
        vander_monde_s = IVRestrictedAI.compute_v(z=s[:idx + 1], e=e[:idx + 1])
        vander_monde_s = IVRestrictedAI.fill_matrix_will_all_s(vander_monde_s.copy(), s[idx + 1:], e[:idx + 1])
        vander_monde_s, operations_s = vander_monde_s.row_echelon_full_matrix()
        if vander_monde.rank() < vander_monde_s.rank():
            return e[idx].count('1')
        r_s = vander_monde_s.rank()
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

        for i in range(len(self.t_table)):
            if self.t_table[i] == 1:
                true_idxs.append(bin(s[i])[2:].zfill(self.n))
            else:
                false_idxs.append(bin(s[i])[2:].zfill(self.n))
            s_bin.append(bin(s[i])[2:].zfill(self.n))
        return true_idxs, false_idxs, s_bin

    @classmethod
    def algebraic_immunity(cls, truth_table: List[int], s: List[int], _hide=False) -> int:
        f_ummu = IVRestrictedAI(truth_table=truth_table)
        z, z_c, s_bin = f_ummu.compute_z(s)
        if z == [] or z_c == []:
            return 0
        e = cls.compute_monomials(n=f_ummu.n, r=f_ummu.n)
        args = [
            (z, z_c, e, s_bin),
            (z_c, z, e, s_bin)
        ]
        #imm1 = f_ummu.find_min_annihilator(z, z_c, e, s_bin)

        #imm2 = f_ummu.find_min_annihilator(z_c, z, e, s_bin)

        #results = [imm1, imm2]
        with Pool() as pool:
            results = pool.starmap(f_ummu.find_min_annihilator, args)
        return min([item for item in results if item is not None])

    @classmethod
    def algebraic_immunity_dist(cls, s_image: List[int], s: List[int], n_vars: int, _verbose: bool = False,
                                _hide: bool = False) -> int:
        f_ummu = IVRestrictedAI(truth_table=s_image, n_vars=n_vars)
        if len(set(f_ummu.t_table)) == 1:
            return int(0)

        z, z_c, s_bin = f_ummu.compute_z_for_dist(s)
        e = cls.compute_monomials(n=f_ummu.n, r=f_ummu.n)

        args = [
                (z, z_c, e, s_bin),
                (z_c, z, e, s_bin)
        ]
        with Pool() as pool:
            results = pool.starmap(f_ummu.find_min_annihilator, args)
        return min([item for item in results if item is not None])

