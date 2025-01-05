import itertools
import json
import math
from sage.all import *
import random

from pathlib import Path
from typing import Union, List

from pydantic import BaseModel

from restricted_algebraic_immunity import settings



from restricted_algebraic_immunity.utils.logging import get_logger
from restricted_algebraic_immunity.utils.utils import partition

log = get_logger(__name__)


class TruthTable(BaseModel):
    __root__: List[Union[int]]

    class Config:
        arbitrary_types_allowed = True


class TruthTables(BaseModel):
    size: int
    tables: List[TruthTable]


class BalancedSlice:

    def __init__(self, k, n_variables, domain):
        max_column = 2 ** n_variables
        self.k = k
        self.n = n_variables
        self.max_column = 2 ** n_variables
        self.domain = domain
        # self.values = values

    def __repr__(self):
        return f"BalancedSlice {self.domain}"
        # vectors_str = ",\n".join([f"\t\t{vec}" for vec in self.vectors])
        # return f"\n\tdomain -> {self.domain}\n\tvalues -> {self.values}\n\tvectors -> [\n{vectors_str}\n\t]"
        # return f"\n\tdomain -> {self.domain}\n\tvalues -> {self.values}\n\tvectors -> {self.vectors}"

    @staticmethod
    def all_fix_hw(n_variables, k):
        it = itertools.combinations(range(n_variables), k)
        return [[1 if i in item else 0 for i in range(n_variables)] for item in it]

    def generate_vectors(self):
        half_n = len(self.domain) // 2
        iter = itertools.combinations(range(len(self.domain)), half_n)
        return [[1 if idx in indexes else 0 for idx,v in enumerate(self.domain)] for indexes in iter]

    def generate_wapb_vectors(self):
        half_n = math.ceil(len(self.domain)/ 2)
        iter = itertools.combinations(range(len(self.domain)), half_n)
        return [[1 if idx in indexes else 0 for idx,v in enumerate(self.domain)] for indexes in iter]

    @staticmethod
    def generate_random_vector(size, k):
        v = [0 for _ in range(size)]
        step = 0
        used_indexes = []
        while step < k:
            rand_idx = random.randint(0, size - 1)
            if rand_idx not in used_indexes:
                v[rand_idx] = 1
                used_indexes.append(rand_idx)
                step += 1
        return v

    def generate_wapb_random_vectors(self, sample_size: int):
        half_n = math.ceil(len(self.domain)/ 2)
        for _ in range(sample_size):
            yield BalancedSlice.generate_random_vector(len(self.domain), half_n)

    def build_wpb_vectors(self, sample_size=None, parallel: bool = False):
        print(f"build_vectors called with self.k={self.k} and self.max_column={self.max_column}")
        if self.k == 0:
            log.debug("Condition met: self.k == 0 or self.k == self.max_column - 1")
            # vect = zero_vector(GF(2), self.max_column)
            # vect[-1] = Integer(1)
            # log.debug(f"Returning vector: {vect}")
            return [vector(GF(2), [0])]
        elif self.k == self.n:
            return [vector(GF(2), [1])]
        else:
            half_n = len(self.domain) // 2
            log.debug("Condition not met, calling self.generate_half_hamming_weight_vectors")
            if len(self.domain) % 2:
                log.error("The length of the vector must be even.")
                raise ValueError("The length of the vector must be even.")
            return [BalancedSlice.generate_random_vector(len(self.domain), half_n) for i in range(sample_size)]







class WPBFamily:

    def __init__(self, m):
        n_var = 2 ** m
        p = partition(n_var)
        self.m = m
        self.n = n_var
        self.slices = [BalancedSlice(n_variables=n_var, k=k, domain=p[k]) for k in range(0, n_var + 1)]

    def __repr__(self):
        return f"WPB {self.n}-variables Boolean function family"

    def build_all_vectors(self, dist_sample):
        return [list(item.build_vectors(sample_size=dist_sample)) for item in self.slices]

    def build_all_tt(self, family_vectors):
        for vectors in itertools.product(*family_vectors):
            summ_vect = add_vectors(*vectors)
            summ_vect[0] = 0
            summ_vect[-1] = 1
            yield summ_vect

    @staticmethod
    def build_all_tt_model(tt_tables):
        size = 0
        tables = []
        for tt_table in tt_tables:
            tables.append(TruthTable(__root__=tt_table))
            size += 1
        return TruthTables(tables=tables, size=size)

    def save_tt_to_file(self, table_list: TruthTables, sub_filename: str = "WPB", dist_sample: str = ""):
        if dist_sample != "":
            dist_sample = "_" + dist_sample
        filename = Path(f"{settings.base_url}/data/truth_tables/{sub_filename}_{self.m}{dist_sample}.json")
        with filename.open("w") as f:
            json.dump(orjson.loads(table_list.json()), f)

    @staticmethod
    def fetch_tt_from_file(m: int, sub_filename: str = "WPB", dist_sample: str = "") -> TruthTables:
        if dist_sample != "":
            dist_sample = "_" + dist_sample
        filename = Path(f"{settings.base_url}/data/truth_tables/{sub_filename}_{m}{dist_sample}.json")
        with filename.open("r") as f:
            resp = json.load(f)
        return TruthTables.parse_obj(resp)




class WAPBFamily:

     def __init__(self, n):
         self.n = n
         p = partition(n)
         self.slices = [BalancedSlice(n_variables=n, k=k, domain=p[k]) for k in range(0, n + 1)]

def add_vectors(*vectors):
    return [sum(components) for components in zip(*vectors)]


if __name__ == '__main__':
    for n in range(1,10):
        k = math.ceil(n /2)
        wapb_family = WAPBFamily(n=n)
        slice_ = wapb_family.slices[k]
        if n <= 6:
            vectors = slice_.generate_wapb_vectors()
            print(vectors)
    print()

# x : w(x) = k   k = 0, 2^m