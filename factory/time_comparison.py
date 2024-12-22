import math
import multiprocessing
import os
import time

import pandas as pd

from WPB_constructor import WAPBFamily
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger()


def run_immunity(method, vector, domain, n):
    t = time.time()
    ai_k = method(vector, domain, n)
    dt = time.time() - t
    return dt

class TimeMeasurement:

    @staticmethod
    def measure_time_for_ai_e_n_half_by_alg(alg, max_n: int = 17, sample_size: int = 1000, parallel=False):
        method = getattr(alg, "algebraic_immunity_dist")

        times = {}
        ai_ks_d = {}

        for n in range(1, max_n):
            times[n] = 0
            k = math.ceil(n / 2)
            wapb_family = WAPBFamily(n=n)
            slice_ = wapb_family.slices[k]
            if n <= 5:
                vectors = slice_.generate_wapb_vectors()
                _log.info(f'restricted truth tables generated for n={n}. Number of item: {len(vectors)}')
                t_n = []
                ai_ks = []
                for vector in vectors:
                    t = time.time()
                    ai_k = method(vector, slice_.domain, n)
                    dt = time.time() - t
                    t_n.append(dt)
                    ai_ks.append(ai_k)
                    _log.debug(f"AIk calculated for restricted truth table {vector} in {dt} seconds")
                times[n] = sum(t_n) / len(vectors)
                ai_ks_d[n] = sum(ai_ks) / len(vectors)
                _log.info(f"AIk calculated on all restricted truth table of {n} variables. Average time: {times[n]}")
            else:
                t_n = []
                ai_ks = []
                counter = 0
                vectors = list(slice_.generate_wapb_random_vectors(sample_size=sample_size))
                _log.info("GENERATED ALL VECTORS")

                args = [(method,vector, slice_.domain, n) for vector in vectors]
                if parallel is True:

                    tot_cores = os.cpu_count()
                    max_processors = tot_cores // 2
                    with multiprocessing.Pool(processes=max_processors) as pool:
                        result = pool.starmap(run_immunity, args)
                    times[n] = sum(result) / len(vectors)

                else:
                    for vector in vectors:
                        t = time.time()
                        ai_k = method(vector, slice_.domain, n)
                        dt = time.time() - t
                        t_n.append(dt)
                        ai_ks.append(ai_k)
                        counter += 1
                        _log.debug(f"AIk calculated for restricted truth table {vector} in {dt} seconds")
                        times[n] = sum(t_n) / counter
                # ai_ks_d[n] = sum(ai_ks) / counter
                _log.info(f"AIk calculated on all restricted truth table of {n} variables. Average time: {times[n]}")
        df_times = pd.DataFrame(times.items(), columns=["n", r"$T(AI_{n/2})$"])
        # df_ai_k = pd.DataFrame(ai_ks_d.items(), columns=["n", r"$AI_{n/2}$"])
        return df_times, None
