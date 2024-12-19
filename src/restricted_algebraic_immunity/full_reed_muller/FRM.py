import enum
from multiprocessing import Pool
from typing import List, Tuple

from numpy.lib.function_base import iterable
from sage.all import *
from sage.crypto.boolean_function import BooleanFunction
from sage.rings.integer import Integer

from restricted_algebraic_immunity import settings
from restricted_algebraic_immunity.entities.enums import FileName


class FRMRestrictedAI:

    def __init__(self):
        rm = load(f"{settings.root_path}/full_reed_muller/pre_computation/{FileName.REED_MILLER.value}.sobj")
        degrees = load(f"{settings.root_path}/full_reed_muller/pre_computation/{FileName.DEGREES.value}.sobj")
        self.degrees = degrees
        self.reed_millers = rm

    @staticmethod
    def find_annililhiator(s, m, m_s, rows):
        r = 0
        d = 1
        max_rank = ceil(len(s) / 2)
        while r <= max_rank:
            n_r = rows[d]
            sub_m = m[:n_r]
            r = sub_m.rank()
            sumb_ms = m_s[:n_r]
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
    def get_gen_matrices(f: BooleanFunction, m: Matrix, s) -> Tuple[Matrix, Matrix]:
        tab = f.truth_table()
        tb = (tab[idx] for idx in s)
        a, b = zip(*[(m.column(i), None) if next(tb) == 0 else (None, m.column(i)) for i in range(len(s))])
        m1 = Matrix(filter(lambda v: v is not None, a)).T
        m2 = Matrix(filter(lambda v: v is not None, b)).T
        return m1, m2

    @staticmethod
    def get_gen_matrices_dist(f_z: List, m: Matrix, s) -> Tuple[Matrix, Matrix]:
        tb = iter(tuple(f_z))
        a, b = zip(*[(m.column(i), None) if next(tb) == 0 else (None, m.column(i)) for i in range(len(s))])
        m1 = Matrix(filter(lambda v: v is not None, a)).T
        m2 = Matrix(filter(lambda v: v is not None, b)).T
        return m1, m2

    @staticmethod
    def extract_restriction(s: List[Integer], m):
        columns = m.columns()
        restriction = [columns[idx] for idx in s]
        return restriction, Matrix(restriction).transpose()

    def algebraic_immunity(self, f: BooleanFunction, s: List) -> Integer:
        tb = f.truth_table()
        n = log(len(tb), 2)
        submatrix = self.reed_millers[n]
        restriction, mat = FRMRestrictedAI.extract_restriction(s=s, m=submatrix)
        if len(set([tb[i] for i in s])) == 1:
            return 0
        degrees = self.degrees[n]
        reed_miller_f_generator, reed_miller_g_generator = FRMRestrictedAI.get_gen_matrices(f=f, m=mat, s=s)
        args_to_processes = [(s, reed_miller_f_generator, mat, degrees), (s, reed_miller_g_generator, mat, degrees)]
        return FRMRestrictedAI.run_processes(args_to_processes)

    def algebraic_immunity_dist(self, s_image: List, s: List, n_vars: int) -> Integer:
        submatrix = self.reed_millers[n_vars]
        restriction, mat = FRMRestrictedAI.extract_restriction(s=s, m=submatrix)
        if len(set(s_image)) == 1:
            return int(0)
        degrees = self.degrees[n_vars]
        reed_miller_f_generator, reed_miller_g_generator = FRMRestrictedAI.get_gen_matrices_dist(f_z=s_image, m=mat, s=s)
        args_to_processes = [(s, reed_miller_f_generator, mat, degrees), (s, reed_miller_g_generator, mat, degrees)]
        return FRMRestrictedAI.run_processes(args_to_processes)
