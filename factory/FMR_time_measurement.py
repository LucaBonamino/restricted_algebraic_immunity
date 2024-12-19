import argparse
import math
import os
import time

import pandas as pd

from WPB_constructor import WAPBFamily
from restricted_algebraic_immunity.full_reed_muller.FRM import FRMRestrictedAI
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)


class TimeMeasurement:

    @staticmethod
    def measure_time_for_ai_e_n_half_by_alg(alg, max_n: int = 17, sample_size: int = 1000):
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
                    ai_k = getattr(alg, "algebraic_immunity_dist")(vector, slice_.domain, n)
                    # ai_k = IVRestrictedAI.algebraic_immunity_dist(s_image=vector, s=slice_.domain, n_vars=n)
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
                for vector in slice_.generate_wapb_random_vectors(sample_size=sample_size):
                    t = time.time()
                    ai_k = getattr(alg, "algebraic_immunity_dist")(vector, slice_.domain, n)
                    dt = time.time() - t
                    t_n.append(dt)
                    ai_ks.append(ai_k)
                    counter += 1
                    _log.debug(f"AIk calculated for restricted truth table {vector} in {dt} seconds")
                times[n] = sum(t_n) / counter
                ai_ks_d[n] = sum(ai_ks) / counter
                _log.info(f"AIk calculated on all restricted truth table of {n} variables. Average time: {times[n]}")
        df_times = pd.DataFrame(times.items(), columns=["n", r"$T(AI_{n/2})$"])
        df_ai_k = pd.DataFrame(ai_ks_d.items(), columns=["n", r"$AI_{n/2}$"])
        return df_times, df_ai_k


class FMRTimeMeasurement(TimeMeasurement):

    @staticmethod
    def measure_time_for_ai_e_n_half(max_n: int = 17, sample_size: int = 1000):
        im = FRMRestrictedAI()

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
                    ai_k = im.algebraic_immunity_dist(s_image=vector, s=slice_.domain, n_vars=n)
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
                for vector in slice_.generate_wapb_random_vectors(sample_size=sample_size):
                    t = time.time()
                    ai_k = im.algebraic_immunity_dist(s_image=vector, s=slice_.domain, n_vars=n)
                    dt = time.time() - t
                    t_n.append(dt)
                    ai_ks.append(ai_k)
                    counter += 1
                    _log.debug(f"AIk calculated for restricted truth table {vector} in {dt} seconds")
                times[n] = sum(t_n) / counter
                ai_ks_d[n] = sum(ai_ks) / counter
                _log.info(f"AIk calculated on all restricted truth table of {n} variables. Average time: {times[n]}")
        df_times = pd.DataFrame(times.items(), columns=["n", r"$T(AI_{n/2})$"])
        df_ai_k = pd.DataFrame(ai_ks_d.items(), columns=["n", r"$AI_{n/2}$"])
        return df_times, df_ai_k



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Time Calculator',
        description='Calculates the average AIk execution time for k = ceil(n/2) for different values of n',
    )
    parser.add_argument('-N', '--max_n', help='maximum value of n', type=int, default=5)
    parser.add_argument('-O', '--sample_size', help='sample_size', type=int, default=10000)
    args = parser.parse_args()


    times, aik_s = FMRTimeMeasurement.measure_time_for_ai_e_n_half(max_n=args.max_n, sample_size=args.sample_size)
    print(times)
    print()
    print(aik_s)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f"results/FMR/times.csv")
    times.to_csv(file_path, index=False)

    file_path = os.path.join(script_dir, f"results/FMR/ai_ks.csv")
    aik_s.to_csv(file_path, index=False)
