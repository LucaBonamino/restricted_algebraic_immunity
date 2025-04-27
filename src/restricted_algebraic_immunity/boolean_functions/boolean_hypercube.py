import itertools
import time

from restricted_algebraic_immunity.utils.logging import get_logger, set_level
from restricted_algebraic_immunity.utils.utils import partition
from algebraic_immunity_utils import RestrictedAI

_log = get_logger(__name__)

class Slice:

    @staticmethod
    def all_fix_hw(n_variables, k):
        it = itertools.combinations(range(n_variables), k)
        return [[1 if i in item else 0 for i in range(n_variables)] for item in it]

    def __init__(self, k, n_variables, domain):
        self.k = k
        self.n = n_variables
        self.domain =  domain


    def get_s_image(self, truth_table):
        return [int(truth_table[idx]) for idx in range(len(truth_table)) if idx in self.domain]

    @set_level(logger=_log)
    def immunity_k(self, s_image, _verbose: bool = False, _hide: bool = False):
        padded_v = [0 for _ in range(2 ** self.n)]
        for idx, val in zip(self.domain, s_image):
            padded_v[idx] = val
        ti = time.time()
        immunity = RestrictedAI.algebraic_immunity(padded_v, self.domain, self.n)
        dt = time.time() - ti
        _log.info(f"[AIk] Immunity for k = {self.k}: {immunity}")
        return immunity, dt

    @set_level(logger=_log)
    def immunity_f_k(self, f, _verbose: bool = False, _hide: bool = False):
        ti = time.time()
        immunity = RestrictedAI.algebraic_immunity(list(f.truth_table(format='int')), self.domain, self.n)
        dt = time.time() - ti
        _log.info(f"[AIK-f] Immunity from f for k = {self.k}: {immunity}")
        return immunity, dt

class Slices:

    def __init__(self, n_variables):
        p = partition(n_variables)
        self.partition = p
        self.slices = [Slice(n_variables=n_variables, k=k, domain=p[k]) for k in p]

    def __repr__(self):
        s = ""
        for sl in self.slices:
            s += f"{sl.k} => {sl.domain}\n"
        return s
