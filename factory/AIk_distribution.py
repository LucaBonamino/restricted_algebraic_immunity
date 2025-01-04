import argparse
import math
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from sage.all import *

from WPB_constructor import WPBFamily
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class AIkDistribution:

    @staticmethod
    def run_immunity(sub_tt, slice_domain, n_vars):
        t = time.time()
        aik = IVRestrictedAI.algebraic_immunity_dist(s_image=sub_tt,
                                               s=slice_domain, n_vars=n_vars, _hide=True)
        dt = time.time() - t
        _log.info(f"Calculated AIk: dt: {dt}")
        return aik, dt

    @classmethod
    def compute_ai_per_slice_parallel(cls, element, s, n):
        print("Sample size", s)
        immu = {a: 0 for a in range(int(math.ceil(n) / 2) + 1)}
        helf = math.ceil(len(element.domain) / 2)
        if binomial(len(element.domain), helf) <= s:
            vectors = element.generate_wapb_vectors()
        else:
            vectors = element.build_wpb_vectors(sample_size=s, parallel=True)

        _log.info(f"Built all vectors for slice {element.k}: {len(vectors)} elements")

        partial_process_item = partial(cls.run_immunity, slice_domain=element.domain[::-1], n_vars=n)

        workers = multiprocessing.cpu_count() // 2

        with ProcessPoolExecutor(workers) as executor:
            results = list(executor.map(partial_process_item, vectors))
        # print(results)
        _log.info(f"Calculated all AIk for slice k {element.k}")
        ai_k, dts = zip(*results)
        le = len(vectors)
        for ai in ai_k:
            immu[ai] += 1/le
        _log.info(f"Average time: {sum(dts) / len(vectors)}")
        return immu, sum(dts) / len(vectors), sum(ai_k)/len(vectors),

        # for vector in vectors:
        #     v = list(vector)
        #     _log.info(f"Starting calculation of AIk for k={element.k} vector {size}")
        #     t = time.time()
        #     immunity = IVRestrictedAI.algebraic_immunity_dist(s_image=v,
        #                                                       s=element.domain[::-1], n_vars=n, _hide=True)
        #     dt = time.time() - t
        #     # imm_2 = FRMRestrictedAI().algebraic_immunity_dist(s_image=v, s=element.domain[::-1], n_vars=n)
        #     # assert imm_2 == immunity
        #     tim.append(dt)
        #     ai_k += immunity
        #     # immunity = calculate_ai(f=list(vector), s=element.domain[::-1], obj=EfficientAIRestrictedSet,
        #     #                       method='algebraic_immunity_dist')
        #     _log.info(f"Immunity calculated: {immunity}")
        #     immu[immunity] += 1
        #     size += 1
        #     _log.info(f"Calculated AIk on a vector on the slice of k = {element.k}")
        # return element.k, {k: v / size for k, v in immu.items()}, sum(tim) / len(tim), ai_k / len(vectors)

    @staticmethod
    def compute_ai_per_slice(element, s, n):
        immu = {a: 0 for a in range(int(math.ceil(n) / 2) + 1)}
        size = 0
        print("Sample size", s)
        vectors = element.build_wpb_vectors(sample_size=s, parallel=True)
        tim = 0
        ai_k = 0
        for idx,vector in enumerate(vectors):
            v = list(vector)
            _log.info(f"Starting calculation of AIk for k={element.k} vector {size}")
            t = time.time()
            immunity = IVRestrictedAI.algebraic_immunity_dist(s_image=v,
                                                              s=element.domain[::-1], n_vars=n, _hide=True)
            dt = time.time() - t
            print(dt)
            # imm_2 = FRMRestrictedAI().algebraic_immunity_dist(s_image=v, s=element.domain[::-1], n_vars=n)
            # assert imm_2 == immunity
            tim += dt
            ai_k += immunity
            _log.info(f"Immunity calculated: {immunity}")
            immu[immunity] += 1
            size += 1
            _log.info(f"Calculated AIk on a vector on the slice of k = {element.k}")
        print(tim/len(vectors))
        return element.k, {k: v / size for k, v in immu.items()}, tim/len(vectors), ai_k / len(vectors)

    @staticmethod
    def dict_to_aik_df(data):
        dfs = []
        df_dict = {}
        for k, v in data.items():
            v_l = list(v)
            df = pd.DataFrame({
                r'$k$': [k for _ in range(len(v_l))],
                r'$AI_k(f)=d$': list(v.keys()),
                r'$p\left(AI_K(f) = d\right)$': list(v.values())
            })
            dfs.append(df)
            df_dict[k] = df
        return df_dict, pd.concat(dfs, ignore_index=True)

    @classmethod
    def func_parallel(cls, m: int, s: int, n: int):

        family = WPBFamily(m=m)
        partial_process_item = partial(cls.compute_ai_per_slice, s=s, n=n)

        workers = multiprocessing.cpu_count() // 2

        with ProcessPoolExecutor(workers) as executor:
            results = list(executor.map(partial_process_item, family.slices))
        k, probs, times, averages = list(zip(*results))
        prob_dict = {k[i]: probs[i] for i in range(len(probs))}
        df_2 = cls.dict_to_aik_df(data=prob_dict)

        df_times = pd.DataFrame({
            r'$k$': k,
            r'$\mathbb{E}[T(AI_k)]$': times,
            r'$\mathbb{E}[AI_k]$': averages
        })

        df_averages = pd.DataFrame({
            'k': k,
            'average': averages
        })
        return df_2, df_times, df_averages

    @classmethod
    def func_parallel_seq(cls, m: int, s: int, n: int, k_range: List[int]):
        family = WPBFamily(m=m)

        prob, times, average = {}, {}, {}
        slices = family.slices
        for k in k_range:
            item = slices[k]
        # for item in family.slices:
            prob_by_k, times_by_k, average_by_k = cls.compute_ai_per_slice_parallel(element=item, s=s, n=n)
            prob[item.k] = prob_by_k
            times[item.k] = times_by_k
            average[item.k] = average_by_k

        df_2 = cls.dict_to_aik_df(data=prob)
        k = [item for item in k_range]
        df_times = pd.DataFrame({
            r'$k$': k,
            r'$\mathbb{E}[T(AI_k)]$': times.values(),
            r'$\mathbb{E}[AI_k]$': average.values()
        })

        df_averages = pd.DataFrame({
            'k': k,
            'average': average.values()
        })
        return df_2, df_times, df_averages

    @staticmethod
    def plot_dist(distribution_data, n, sample_size, save: bool = True,
                  parallelization_type: str = "", max_k: str = "", min_k: str = ""):
        # filename = tables_dir / f"table_m_{m}_sample_size_{sample_size}"

        main_vals = distribution_data[0]
        prob_vals = distribution_data[1]
        # prob_vals = {
        #     '0': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [1, 0, 0, 0, 0]
        #     }),
        #     '1': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 1, 0, 0, 0]
        #     }),
        #     '2': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 0.046051, 0.953949, 0, 0]
        #     }),
        #     '3': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 0, 0.983856, 0.016144, 0]
        #     }),
        #     '4': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 0, 0.125275, 0.874725, 0]
        #     }),
        #     '5': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 0, 0.983673, 0.016327, 0]
        #     }),
        #     '6': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 0.048401, 0.951599, 0, 0]
        #     }),
        #     '7': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [0, 1, 0, 0, 0]
        #     }),
        #     '8': pd.DataFrame({
        #         "$AI_k(f)=d$": [0, 1, 2, 3, 4],
        #         r'$p\left(AI_K(f) = d\right)$': [1, 0, 0, 0, 0]
        #     }),
        # }
        m = math.log(n, 2)

        fig, ax = plt.subplots()
        print(main_vals)
        ax.set_title(fr'Average of $AI_{{k}}$ for $n={n}$, $m={m}$ and sample_size$={sample_size}$')
        ax.plot(main_vals['k'], main_vals['average'])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel('k')
        ax.set_ylabel(r'$\mu_{AI_k}$', rotation=0)
        ax.grid()
        if save is True:
            plot_filename = Path(
                os.path.join(SCRIPT_DIR,
                             f"results/IV/AIk_distributions/WPB_{m}_sample_size_{sample_size}_dist_{parallelization_type}_{min_k}_{max_k}.png"))
            plt.savefig(str(plot_filename))
        plt.close()

        fig, ax = plt.subplots()
        ax.set_title(fr'Distribution of $AI_{{k}}$ for $n={n}$ and sample_size$={sample_size}$')
        for k, v in prob_vals.items():
            print(v)
            ax.plot(v['$AI_k(f)=d$'], v[r'$p\left(AI_K(f) = d\right)$'], marker='x',
                    label=fr'$k={k} \Rightarrow E_{{{k},{n}}}$')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel(r'$AI_k$')
        ax.set_ylabel(r'$p\left({AI_k}\right)$', rotation=0)
        ax.grid()
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True,
                  ncol=len(prob_vals.keys()) // 2)
        plt.tight_layout()
        # Use tight_layout
        if save is True:
            plot_filename = Path(
                os.path.join(SCRIPT_DIR,
                             f"results/IV/AIk_distributions/WPB_{m}_sample_size_{sample_size}_dist_prob_{parallelization_type}.png"))
            plt.savefig(str(plot_filename))
        plt.close(fig)

    @classmethod
    def func_parallel_non_parallel(cls, m: int, s: int, n: int, k_range: List[int]):
        ais = {k: 0 for k in range(n + 1)}
        probs = {k: 0 for k in range(n + 1)}
        family = WPBFamily(m=m)
        times = {k: 0 for k in range(n + 1)}
        slices = family.slices
        for k in k_range:
            element = slices[k]
        # for element in family.slices:
            helf = math.ceil(len(element.domain) / 2)
            if binomial(len(element.domain), helf) <= s:
                vectors = element.generate_wapb_vectors()
            else:
                vectors = element.build_wpb_vectors(sample_size=s, parallel=True)
            _log.info(f"{len(vectors)} build")
            prob = {a: 0 for a in range(int(math.ceil(n) / 2) + 1)}
            vals = 0
            size = 0
            ti = 0
            for idx,v in enumerate(vectors):
                if idx % 1000 == 0:
                    _log.info(f"iteration: {idx}")
                t = time.time()
                immunity = IVRestrictedAI.algebraic_immunity_dist(s_image=v,
                                                                  s=element.domain[::-1], n_vars=n, _hide=True)
                dt = time.time() - t
                _log.debug(f"execution time: {dt}")
                ti += dt
                vals += immunity
                size += 1
                prob[immunity] += 1
            times[element.k] = ti / size
            _log.info(f"average time for k={element.k}: {times[element.k]}")
            ais[element.k] = vals / size
            probs[element.k] = {k: v / size for k, v in prob.items()}
            # counts = Counter(results)
            # probs[element.k] = {i: counts.get(i, 0) / len(results) for i in range(n + 1)}
        ks = [item.k for item in family.slices]
        df_times = pd.DataFrame({
            r'$k$': [item.k for item in family.slices],
            r'$\mathbb{E}[T(AI_k)]$': times.values()
        })
        df_averages = pd.DataFrame({
            'k': ks,
            'average': ais.values()
        })

        probs_df = cls.dict_to_aik_df(data=probs)
        return probs_df, df_times,df_averages


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
    parser.add_argument('-p', '--parallelize_by', type=str, default='slice')
    parser.add_argument('-kM', '--k_max', type=int, default=None)
    parser.add_argument('-km', '--k_min', type=int, default=0)
    parser.add_argument('-pl', '--plot', action='store_true', help="Plot results")
    args = parser.parse_args()

    slice_k = list(range(args.n_vars + 1))

    if args.k_max is not None:
        if args.k_max != args.k_min:
            slice_k = list(range(args.k_min, args.k_max+1))
        else:
            slice_k = [args.k_min]
    print(slice_k)
    m_log = int(math.log(args.n_vars, 2))
    if args.parallelize_by == 'slice':
        dist_df, times_df, df_averages = AIkDistribution.func_parallel(m=m_log, n=args.n_vars, s=args.sample_size, k_range=slice_k)
    elif args.parallelize_by == 'a':
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=args.n_vars, s=args.sample_size, k_range=slice_k)
    else:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_non_parallel(m=m_log, n=args.n_vars, s=args.sample_size, k_range=slice_k)
        # dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=args.n_vars, s=args.sample_size)
    times_latex = times_df.to_latex(index=False, escape=False)

    file_path = Path(
        os.path.join(SCRIPT_DIR, f"results/IV/AIk_distributions/times_n_{args.n_vars}_sample_{args.sample_size}_{args.parallelize_by}_{args.k_min }_{args.k_max }.txt"))
    save_raw_data_to_file(filename=file_path, data=times_latex)
    print(dist_df)
    dist_latex = dist_df[1].to_latex(index=False, escape=False)
    if args.plot is True:
        AIkDistribution.plot_dist(distribution_data=(df_averages, dist_df[0]), sample_size=args.sample_size, n=args.n_vars,
                              save=True, parallelization_type=args.parallelize_by, max_k=str(args.k_max), min_k=str(args.k_min))
    # AIkDistribution.plot_dist(distribution_data=(None, None), sample_size=args.sample_size, n=args.n_vars,
    #                          save=True)
    file_path = Path(
        os.path.join(SCRIPT_DIR,
                     f"results/IV/AIk_distributions/distribution_n_{args.n_vars}_sample_{args.sample_size}_{args.parallelize_by}_{args.k_min }_{args.k_max }.txt"))
    save_raw_data_to_file(filename=file_path, data=dist_latex)

    file_path = Path(
        os.path.join(SCRIPT_DIR,
                     f"results/IV/AIk_distributions/distribution_n_{args.n_vars}_sample_{args.sample_size}_{args.parallelize_by}_{args.k_min}_{args.k_max}_averages.txt"))
    averages_latex = df_averages.to_latex(index=False, escape=False)
    save_raw_data_to_file(filename=file_path, data=averages_latex)