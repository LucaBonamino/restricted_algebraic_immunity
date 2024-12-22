import time
from typing import Dict, List
from sage.all import *

from restricted_algebraic_immunity import settings


def compute_generator_matrix(n, r):
    return codes.BinaryReedMullerCode(r, n).generator_matrix()

def pre_compute_all_matrices(n, restricted=False):
    if restricted:
        d = {i: compute_generator_matrix(n=i, r=i) for i in range(2, n + 1)}
    else:
        d = {i: compute_generator_matrix(n=i, r=ceil(i / 2) - 1) for i in range(2, n + 1)}
    d.update({1: compute_generator_matrix(n=1, r=0)})
    return d


def pre_compute_degrees(n, restricted=False):
    if restricted:
        deg = {i: {j: sum([binomial(i, k) for k in range(j + 1)]) for j in range(i + 1)} for i in range(2, n + 1)}
    else:
        deg = {i: {j: sum([binomial(i, k) for k in range(j + 1)]) for j in range(ceil(i / 2)+1)} for i in range(2, n + 1)}
    deg.update({1: {j: sum([binomial(1, k) for k in range(j + 1)])} for j in range(2)})
    return deg

def pre_compute_all(n_vars):
    t = time.time()
    m = pre_compute_all_matrices(n=n_vars, restricted=True)
    degrees = pre_compute_degrees(n=n_vars, restricted=True)
    dt = time.time() - t
    save_to_matrices_file(m)
    save_deg_to_file(degrees)
    return dt


def save_deg_to_file(d: Dict):
    save(d, f'{settings.root_path}/full_reed_muller/pre_computation/degs.sobj')


def save_to_matrices_file(d: Dict[int, List]):
    save(d, f'{settings.root_path}/full_reed_muller/pre_computation/RMs.sobj')