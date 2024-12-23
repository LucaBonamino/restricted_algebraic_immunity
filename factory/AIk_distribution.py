import argparse
import math
import multiprocessing
import os
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

import pandas as pd

from WPB_constructor import WPBFamily
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)


class AIkDistribution:

    @staticmethod
    def compute_ai_per_slice(element, s, n):
        immu = {idx: 0 for idx in range(n + 1)}
        size = 0
        print("Sample size", s)
        vectors = list(element.build_wpb_vectors(sample_size=s, parallel=True))
        tim = []
        ai_k = 0
        for vector in vectors:
            v = list(vector)
            _log.info(f"Starting calculation of AIk for k={element.k} vector {size}")
            t = time.time()
            immunity = IVRestrictedAI.algebraic_immunity_dist(s_image=v,
                                                              s=element.domain[::-1], n_vars=n, _hide=True)
            dt = time.time() - t
            tim.append(dt)
            ai_k += immunity
            # immunity = calculate_ai(f=list(vector), s=element.domain[::-1], obj=EfficientAIRestrictedSet,
            #                       method='algebraic_immunity_dist')
            _log.info(f"Immunity calculated: {immunity}")
            immu[immunity] += 1
            size += 1
            _log.info(f"Calculated AIk on a vector on the slice of k = {element.k}")
        return element.k, immu, sum(tim) / len(tim), ai_k / len(vectors)
        # return element.k, {ke: v / size for ke, v in immu.items()}, sum(tim) / len(tim), ai_k / len(vectors)

    @classmethod
    def func_parallel(cls, m: int, s: int, n: int):
        # ais = {k: {idx: 0 for idx in range(n + 1)} for k in range(n + 1)}

        family = WPBFamily(m=m)
        partial_process_item = partial(cls.compute_ai_per_slice, s=s, n=n)

        workers = multiprocessing.cpu_count() // 2

        with ThreadPoolExecutor(workers) as executor:
            results = list(executor.map(partial_process_item, family.slices))
        k, probs, times, averages = list(zip(*results))
        print(probs)
        df_dist = pd.DataFrame({
            r'$k$': k,
            r'$p\left(AI_K(f) = d\right)$': list(probs[0].values()),
        })
        df_times = pd.DataFrame({
            r'$k$': k,
            r'$\mathbb{E}[T(AI_k)]$': times,
            r'$\mathbb{E}[AI_k]$': averages
        })
        return df_dist, df_times


def save_raw_data_to_file(filename: Path, data: str):
    with filename.open('w') as file:
        file.write(data)


if __name__ == '__main__':
    # print(multiprocessing.cpu_count())
    parser = argparse.ArgumentParser(
        prog='AIk Distribution Calculator',
        description='Compute the AIk distribution of WPB functions',
    )
    parser.add_argument('-n', '--n_vars', help='number of variables', type=int, default=8)
    parser.add_argument('-O', '--sample_size', help='sample_size', type=int, default=10)
    args = parser.parse_args()
    m_log = int(math.log(args.n_vars, 2))
    dist_df, times_df = AIkDistribution.func_parallel(m=m_log, n=args.n_vars, s=args.sample_size)
    times_latex = times_df.to_latex(index=False, escape=False)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = Path(
        os.path.join(script_dir, f"results/IV/AIk_distributions/times_n_{args.n_vars}_sample_{args.sample_size}.txt"))
    save_raw_data_to_file(filename=file_path, data=times_latex)

    dist_latex = dist_df.to_latex(index=False, escape=False)
    file_path = Path(
        os.path.join(script_dir, f"results/IV/AIk_distributions/distribution_n_{args.n_vars}_sample_{args.sample_size}.txt"))
    save_raw_data_to_file(filename=file_path, data=dist_latex)

