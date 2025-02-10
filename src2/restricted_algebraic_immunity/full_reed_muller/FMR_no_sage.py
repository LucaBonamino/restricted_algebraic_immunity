from multiprocessing import Pool
from typing import List, Tuple

from algebraic_immunity_utils import Matrix as GF2Matrix
from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
from sage.rings.integer import Integer

from restricted_algebraic_immunity import settings
from restricted_algebraic_immunity.entities.enums import FileName
from restricted_algebraic_immunity.utils.file_utils import load_large_bit_matrix_bin


def from_sage_to_list(m):
    return [list(row) for row in m.rows()]


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


class FRMRestrictedAINoSage:

    def __init__(self, n_max: int):
        try:
            print("I am here")
            file_name = f"{settings.root_path}/full_reed_muller/pre_computation/largeMatrices/large_bit_matrix_{n_max}.bin"
            mat = load_large_bit_matrix_bin(file_name)
            rm = {n_max: mat.tolist()}
            degrees = load(
                f"{settings.root_path}/full_reed_muller/pre_computation/{FileName.DEGREES.value}_{n_max}.sobj")
        except FileNotFoundError:
            raise Exception(
                f"Reed Muller generator matrix not pre-computed for n_max = {n_max}. "
                f"Pre-compute it before computing the AIk")
        self.degrees = degrees
        self.reed_millers = rm

    @staticmethod
    def find_annililhiator(s, m, m_s, rows):
        m = GF2Matrix(m)
        m_s = GF2Matrix(m_s)
        r = 0
        d = 1
        max_rank = ceil(len(s) / 2)
        while r <= max_rank:
            n_r = rows[d]
            sub_m, _ = m.get_sub_matrix(0, n_r).row_echelon_full_matrix()
            r = sub_m.rank()
            sumb_ms, _ = m_s.get_sub_matrix(0, n_r).row_echelon_full_matrix()
            r_s = sumb_ms.rank()
            if r < r_s:
                return d
            else:
                d += 1

    @classmethod
    def run_processes(cls, args):
        with Pool() as pool:
            results = pool.starmap(cls.find_annililhiator, args)
        return min(filter(lambda item: item is not None, results))

    @staticmethod
    def get_gen_matrices(f: BooleanFunction, m: List, s) -> Tuple[GF2Matrix, GF2Matrix, GF2Matrix]:
        tab = f.truth_table()
        tb = [tab[idx] for idx in s]
        s_matrix = []
        m1 = []
        m2 = []
        for i in range(len(m)):
            s_matrix.append([])
            m1.append([])
            m2.append([])
            for j in s:
                el = m[i][j]
                s_matrix[i].append(el)
                if tab[j] == 1 or tab[j] is True:
                    m1[i].append(el)
                else:
                    m2[i].append(el)
        return m1, m2, s_matrix
        # a, b = zip(*[(m.column(i), None) if next(tb) == 0 else (None, m.column(i)) for i in range(len(s))])
        # m1 = Matrix(filter(lambda v: v is not None, a)).T
        # m2 = Matrix(filter(lambda v: v is not None, b)).T
        # return m1, m2

    @staticmethod
    def get_gen_matrices_dist(f_z: List, m: Matrix, s) -> Tuple[Matrix, Matrix]:
        tb = iter(tuple(f_z))
        m1_columns = [
            [row[i] for row in m] for i, value in enumerate(tb) if value == 0
        ]
        m2_columns = [
            [row[i] for row in m] for i, value in enumerate(tb) if value == 1
        ]

        m1 = list(map(list, zip(*m1_columns))) if m1_columns else [[] for _ in range(len(matrix))]
        m2 = list(map(list, zip(*m2_columns))) if m2_columns else [[] for _ in range(len(matrix))]

        return m1, m2
        # a, b = zip(*[(m.column(i), None) if next(tb) == 0 else (None, m.column(i)) for i in range(len(s))])
        # m1 = Matrix(filter(lambda v: v is not None, a)).T
        # m2 = Matrix(filter(lambda v: v is not None, b)).T
        # return m1, m2

    @staticmethod
    def extract_restriction(s: List[Integer], m):
        columns = m.columns()
        restriction = [columns[idx] for idx in s]
        return restriction, Matrix(restriction).transpose()

    def algebraic_immunity(self, f: BooleanFunction, s: List) -> Integer:
        tb = f.truth_table()
        n = log(len(tb), 2)
        submatrix = self.reed_millers[n]
        print("HERE")
        if len(set([tb[i] for i in s])) == 1:
            return 0

        print("data loaded")
        degrees = self.degrees[n]
        # mat_list = from_sage_to_list(submatrix)
        reed_miller_f_generator, reed_miller_g_generator, mat = FRMRestrictedAINoSage.get_gen_matrices(f=f, m=submatrix,
                                                                                                       s=s)
        print("DONE he step")
        args_to_processes = [(s, reed_miller_f_generator, mat, degrees), (s, reed_miller_g_generator, mat, degrees)]
        return FRMRestrictedAINoSage.run_processes(args_to_processes)

    def algebraic_immunity_dist(self, s_image: List, s: List, n_vars: int) -> Integer:
        submatrix = self.reed_millers[n_vars]
        restriction, mat = FRMRestrictedAI.extract_restriction(s=s, m=submatrix)
        if len(set(s_image)) == 1:
            return int(0)
        degrees = self.degrees[n_vars]
        reed_miller_f_generator, reed_miller_g_generator = FRMRestrictedAI.get_gen_matrices_dist(f_z=s_image, m=mat,
                                                                                                 s=s)
        args_to_processes = [(s, reed_miller_f_generator, mat, degrees), (s, reed_miller_g_generator, mat, degrees)]
        return FRMRestrictedAI.run_processes(args_to_processes)
