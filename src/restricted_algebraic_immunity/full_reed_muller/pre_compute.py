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
    save_to_matrices_file(m, n_vars)
    save_deg_to_file(degrees, n_vars)
    return dt

def pre_compute_all_separated(n_vars):
    t = time.time()
    m = pre_compute_all_matrices(n=n_vars, restricted=True)
    dt_m = time.time() - t
    t = time.time()
    degrees = pre_compute_degrees(n=n_vars, restricted=True)
    dt_d = time.time() - t
    save_to_matrices_file(m, n_vars)
    save_deg_to_file(degrees)
    return dt_m, dt_d


def save_deg_to_file(d: Dict, n):
    save(d, f'{settings.root_path}/full_reed_muller/pre_computation/degs_n_max_{n}.sobj')


def save_to_matrices_file(d: Dict[int, List], n: int):
    save(d, f'{settings.root_path}/full_reed_muller/pre_computation/RMs_n_max_{n}.sobj')


def pre_compute_by_n_vars(n: int):
    mat = compute_generator_matrix(n=n, r=n)
    deg = {j: sum([binomial(n, k) for k in range(j + 1)]) for j in range(n + 1)}
    save({n: mat}, f'{settings.root_path}/full_reed_muller/pre_computation/RMs_{n}.sobj')
    save({n: deg}, f'{settings.root_path}/full_reed_muller/pre_computation/degs_{n}.sobj')

def pre_compute_by_max_n_vars(n: int):
    pre_compute_all(n)