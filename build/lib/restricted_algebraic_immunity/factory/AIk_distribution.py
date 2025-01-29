import argparse
import enum
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path
from typing import List, Tuple, Dict
import math

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator
from sage.all import *
from sage.crypto.boolean_function import BooleanFunction

from restricted_algebraic_immunity import settings
from restricted_algebraic_immunity.factory.WPB_constructor import WPBFamily, BalancedSlice
from restricted_algebraic_immunity.full_reed_muller.FRM import FRMRestrictedAI
from restricted_algebraic_immunity.inductive_reed_muller.IV import IVRestrictedAI
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class DFKeys(enum.Enum):
    K = 'k'
    AIK = 'aik'
    AIK_DIST = 'aik_distribution'
    AVERAGE_T = 'average_execution_time'
    AVERAGE_AIK = 'average_aik'


class ParallelizationType(enum.Enum):
    SLICES = 'slices'
    SAMPLES = 'a'
    SEQUENCIAL = 'sequencial'


class Algorithm(enum.Enum):
    FRM = '1'
    IV = '3'


class AIkDistribution:

    @staticmethod
    def run_immunity(sub_tt: List[int], slice_domain: List[int], n_vars: int, algorithm: Algorithm,
                     assert_wpb: bool = True, padded_sub_tt: bool = False):
        if assert_wpb is True:
            assert len([item for item in sub_tt if item == 1]) == len(sub_tt) / 2
        if algorithm == Algorithm.FRM:
            immu_obj = FRMRestrictedAI(n_max=n_vars)
            if padded_sub_tt is True:
                padded_v = [0 for _ in range(2 ** n_vars)]
                for idx, val in zip(slice_domain, sub_tt):
                    padded_v[idx] = val
                t = time.time()
                aik = immu_obj.algebraic_immunity(f=BooleanFunction(padded_v), s=slice_domain[::-1])
                dt = time.time() - t
            else:
                t = time.time()
                aik = immu_obj.algebraic_immunity_dist(s_image=sub_tt, s=slice_domain[::-1], n_vars=n_vars)
                dt = time.time() - t
        elif algorithm == Algorithm.IV:
            if padded_sub_tt is True:
                padded_v = [0 for _ in range(2 ** n_vars)]
                for idx, val in zip(slice_domain, sub_tt):
                    padded_v[idx] = val
                t = time.time()
                aik = IVRestrictedAI.algebraic_immunity(truth_table=padded_v, s=slice_domain[::-1])
                dt = time.time() - t
            else:
                t = time.time()
                aik = IVRestrictedAI.algebraic_immunity_dist(s_image=sub_tt, s=slice_domain[::-1], n_vars=n_vars)
                dt = time.time() - t
        else:
            raise Exception("Unknown algorithm")
        _log.info(f"Calculated AIk: dt: {dt}")
        return aik, dt

    @classmethod
    def compute_ai_per_slice_parallel(cls, element: BalancedSlice, s: int, n: int, algorithm: Algorithm):
        _log.info(f"Sample_size: {s}")
        immu = {a: 0 for a in range(int(math.ceil(n) / 2) + 1)}
        helf = math.ceil(len(element.domain) / 2)
        if element.k == 0:
            v = [0]
            aik, dt = cls.run_immunity(v, element.domain, n, algorithm, False)
            ai_k = [aik]
            vectors = [v]
            dts = [dt]
        elif element.k == n:
            v = [1]
            aik, dt = cls.run_immunity(v, element.domain, n, algorithm, False)
            ai_k = [aik]
            vectors = [v]
            dts = [dt]
        else:
            if binomial(len(element.domain), helf) <= s:
                vectors = element.generate_wapb_vectors()
            else:
                vectors = element.build_wpb_vectors(sample_size=s)

            _log.info(f"Built all vectors for slice {element.k}: {len(vectors)} elements")
            partial_process_item = partial(cls.run_immunity, slice_domain=element.domain[::-1], n_vars=n,
                                           algorithm=algorithm)

            workers = multiprocessing.cpu_count() // 2

            with ProcessPoolExecutor(workers) as executor:
                results = list(executor.map(partial_process_item, vectors))
            # print(results)
            _log.info(f"Calculated all AIk for slice k {element.k}")
            ai_k, dts = zip(*results)
        le = len(vectors)
        for ai in ai_k:
            immu[ai] += 1 / le
        _log.info(f"Average time: {sum(dts) / len(vectors)}")
        return immu, sum(dts) / len(vectors), sum(ai_k) / len(vectors)

    @staticmethod
    def compute_ai_per_slice(element, s, n, algorithm):

        immu = {a: 0 for a in range(int(math.ceil(n) / 2) + 1)}
        size = 0
        vectors = element.build_wpb_vectors(sample_size=s)
        tim = 0
        ai_k = 0
        for idx, vector in enumerate(vectors):
            v = list(vector)
            _log.info(f"Starting calculation of AIk for k={element.k} vector {size}")
            if algorithm == Algorithm.IV:
                t = time.time()
                immunity = IVRestrictedAI.algebraic_immunity_dist(s_image=v,
                                                                  s=element.domain[::-1], n_vars=n, _hide=True)
                dt = time.time() - t
            elif algorithm == Algorithm.FRM:
                immu_obj = FRMRestrictedAI(n_max=n)
                t = time.time()
                immunity = immu_obj.algebraic_immunity_dist(s_image=v,
                                                            s=element.domain[::-1], n_vars=n)
                dt = time.time() - t
            else:
                raise Exception("Unknown algorithm")
            print(dt)
            tim += dt
            ai_k += immunity
            _log.info(f"Immunity calculated: {immunity}")
            immu[immunity] += 1
            size += 1
            _log.info(f"Calculated AIk on a vector on the slice of k = {element.k}")
        print(tim / len(vectors))
        return element.k, {k: v / size for k, v in immu.items()}, tim / len(vectors), ai_k / len(vectors)

    @staticmethod
    def dict_to_aik_df(data):
        dfs = []
        df_dict = {}
        print(data)
        for k, v in data.items():
            v_l = list(v)
            df = pd.DataFrame({
                DFKeys.K.value: [k for _ in range(len(v_l))],
                DFKeys.AIK.value: list(v.keys()),
                DFKeys.AIK_DIST.value: list(v.values())
            })
            dfs.append(df)
            df_dict[k] = df
        return df_dict, pd.concat(dfs, ignore_index=True)

    @classmethod
    def func_parallel(cls, m: int, s: int, n: int, k_range, algorithm: Algorithm):

        family = WPBFamily(m=m)
        partial_process_item = partial(cls.compute_ai_per_slice, s=s, n=n, algorithm=algorithm)

        workers = multiprocessing.cpu_count() // 2

        slices = [item for item in family.slices if item.k in k_range]

        with ProcessPoolExecutor(workers) as executor:
            results = list(executor.map(partial_process_item, slices))
        k, probs, times, averages = list(zip(*results))
        prob_dict = {k[i]: probs[i] for i in range(len(probs))}
        df_2 = cls.dict_to_aik_df(data=prob_dict)

        df_times = pd.DataFrame({
            DFKeys.K.value: k,
            DFKeys.AVERAGE_T.value: times,
            DFKeys.AVERAGE_AIK.value: averages
        })

        df_averages = pd.DataFrame({
            DFKeys.K.value: k,
            DFKeys.AVERAGE_AIK.value: averages
        })
        return df_2, df_times, df_averages

    @classmethod
    def func_parallel_seq(cls, m: int, s: int, n: int, k_range: List[int], algorithm: Algorithm):
        family = WPBFamily(m=m)
        prob, times, average = {}, {}, {}
        slices = family.slices
        for k in k_range:
            item = slices[k]
            # for item in family.slices:
            prob_by_k, times_by_k, average_by_k = cls.compute_ai_per_slice_parallel(element=item, s=s, n=n,
                                                                                    algorithm=algorithm)
            prob[item.k] = prob_by_k
            times[item.k] = times_by_k
            average[item.k] = average_by_k

        df_2 = cls.dict_to_aik_df(data=prob)
        k = [item for item in k_range]
        df_times = pd.DataFrame({
            DFKeys.K.value: k,
            DFKeys.AVERAGE_T.value: times.values(),
            DFKeys.AVERAGE_AIK.value: average.values()
        })

        df_averages = pd.DataFrame({
            DFKeys.K.value: k,
            DFKeys.AVERAGE_AIK.value: average.values()
        })
        return df_2, df_times, df_averages

    @classmethod
    def plot_dist(cls, distribution_data: Tuple[pd.DataFrame, Dict[int, pd.DataFrame]], n: int, sample_size: int,
                  parallelization_type: str = "", save: bool = False):

        main_vals = distribution_data[0]
        prob_vals = distribution_data[1]

        m = math.log(n, 2)

        cls.plot_aik_average(average_dataframe=main_vals, sample_size=sample_size, n=n, m=int(m),
                             parallelization_type=parallelization_type, save=save)

        cls.plot_prob_distribution(prob_vals=prob_vals, sample_size=sample_size,
                                   parallelization_type=parallelization_type, m=int(m), n=n, save=save)

    @staticmethod
    def plot_aik_average(average_dataframe: pd.DataFrame, sample_size: int, m: int, n: int, parallelization_type: str,
                         save: bool = True):
        fig, ax = plt.subplots()
        print(average_dataframe)
        ax.set_title(fr'Average of $AI_{{k}}$ for $n={n}$, $m={m}$ and $|\Omega |={sample_size}$')
        ax.plot(average_dataframe[DFKeys.K.value], average_dataframe[DFKeys.AVERAGE_AIK.value])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel('k')
        ax.set_ylabel(r'$\mathbb{E}\left(AI_k\right)$', rotation=90)
        ax.grid()
        if save is True:
            plot_filename = Path(f'{settings.distributions_dir_name}/n_{n}/WPB_{m}_sample_size_{sample_size}_average_{parallelization_type}.png')
            # plot_filename = Path(
            #     os.path.join(SCRIPT_DIR,
            #                  f"results/IV/AIk_distributions/n_{n}/WPB_{m}_sample_size_{sample_size}_average_{parallelization_type}.png"))
            plt.savefig(str(plot_filename))
        plt.close()

    @staticmethod
    def plot_prob_distribution(prob_vals, sample_size, n, parallelization_type, m: int, save: bool = True):
        fig, ax = plt.subplots()
        ax.set_title(fr'Distribution of $AI_{{k}}$ for $n={n}$ and $|\Omega |={sample_size}$')
        for k, v in prob_vals.items():
            ax.plot(v['aik'], v['aik_distribution'], marker='x',
                    label=fr'$k={k} \Rightarrow E_{{{k},{n}}}$')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel(r'$AI_k$')
        ax.set_ylabel(r'$p\left({AI_k}\right)$', rotation=90)
        ax.grid()
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True,
                  ncol=len(prob_vals.keys()) // 2)
        plt.tight_layout()
        # Use tight_layout
        if save is True:
            plot_filename = Path(
                f'{settings.distributions_dir_name}/n_{n}/WPB_{m}_sample_size_{sample_size}_dist_prob_{parallelization_type}.png')
            # plot_filename = Path(
            #     os.path.join(SCRIPT_DIR,
            #                  f"results/IV/AIk_distributions/n_{n}/WPB_{m}_sample_size_{sample_size}_dist_prob_{parallelization_type}.png"))
            plt.savefig(str(plot_filename))
        plt.close(fig)

    @classmethod
    def func_parallel_non_parallel(cls, m: int, s: int, n: int, k_range: List[int], algorithm: Algorithm):
        ais = {k: 0 for k in k_range}
        probs = {k: 0 for k in k_range}
        family = WPBFamily(m=m)
        times = {k: 0 for k in k_range}
        slices = family.slices
        for k in k_range:
            element = slices[k]
            # for element in family.slices:
            helf = math.ceil(len(element.domain) / 2)
            if binomial(len(element.domain), helf) <= s:
                vectors = element.generate_wapb_vectors()
            else:
                vectors = element.build_wpb_vectors(sample_size=s)
            _log.info(f"{len(vectors)} build")
            prob = {a: 0 for a in range(int(math.ceil(n) / 2) + 1)}
            vals = 0
            size = 0
            ti = 0
            for idx, v in enumerate(vectors):
                if idx % 1000 == 0:
                    _log.info(f"iteration: {idx}")
                if algorithm == Algorithm.FRM:
                    immu_obj = FRMRestrictedAI(n_max=n)
                    t = time.time()
                    immunity = immu_obj.algebraic_immunity_dist(s_image=v, s=element.domain[::-1], n_vars=n)
                    dt = time.time() - t
                elif algorithm == Algorithm.IV:
                    t = time.time()
                    immunity = IVRestrictedAI.algebraic_immunity_dist(s_image=v, s=element.domain[::-1], n_vars=n)
                    dt = time.time() - t
                else:
                    raise Exception("Unknown algorithm")
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
        ks = k_range
        df_times = pd.DataFrame({
            r'$k$': k_range,
            r'$\mathbb{E}[T(AI_k)]$': times.values()
        })
        df_averages = pd.DataFrame({
            'k': ks,
            'average': ais.values()
        })
        probs_df = cls.dict_to_aik_df(data=probs)
        return probs_df, df_times, df_averages


def save_raw_data_to_file(filename: Path, data: str):
    with filename.open('w') as file:
        file.write(data)


def main(n: int, k_max: int, k_min: int, parallelize_by: ParallelizationType, sample_size: int, plot: bool,
         algorithm: Algorithm):
    slice_k = list(range(n + 1))
    if k_max is not None:
        if k_max != k_min:
            slice_k = list(range(k_min, k_max + 1))
        else:
            slice_k = [k_min]
    _log.info(f"List of k: {slice_k}")
    m_log = int(math.log(n, 2))
    if parallelize_by == ParallelizationType.SLICES:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel(m=m_log, n=n, s=sample_size,
                                                                       k_range=slice_k,
                                                                       algorithm=algorithm)
    elif parallelize_by == ParallelizationType.SAMPLES:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=n, s=sample_size,
                                                                           k_range=slice_k,
                                                                           algorithm=algorithm)
    else:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_non_parallel(m=m_log, n=n,
                                                                                    s=sample_size, k_range=slice_k,
                                                                                    algorithm=algorithm)
        # dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=args.n_vars, s=args.sample_size)
    times_latex = times_df.to_latex(index=False, escape=False)
    # dire = Path(
    #    os.path.join(SCRIPT_DIR, f"../factory/results/IV/AIk_distributions/n_{n}"))
    dire = Path(f"{settings.distributions_dir_name}/n_{n}")
    if not dire.is_dir():
        dire.mkdir()

    file_path = dire / f"times_n_{n}_sample_{sample_size}_{parallelize_by.value}_{k_min}_{k_max}.txt"
    save_raw_data_to_file(filename=file_path, data=times_latex)
    print(dist_df)
    dist_latex = dist_df[1].to_latex(index=False, escape=False)
    if plot is True:
        AIkDistribution.plot_dist(distribution_data=(df_averages, dist_df[0]), sample_size=sample_size,
                                  n=n,
                                  save=True, parallelization_type=parallelize_by.value)

    if k_min == 0 and k_max is None:
        file_name_prefix = f"distribution_n_{n}_sample_{sample_size}_{parallelize_by.value}"
    elif k_max is None:
        file_name_prefix = f"distribution_n_{n}_sample_{sample_size}_{parallelize_by.value}_{k_min}"
    else:
        file_name_prefix = f"distribution_n_{n}_sample_{sample_size}_{parallelize_by.value}_{k_min}_{k_max}"
    file_path = dire / f"{file_name_prefix}.txt"
    save_raw_data_to_file(filename=file_path, data=dist_latex)

    file_path = dire / f"{file_name_prefix}_averages.txt"
    averages_latex = df_averages.to_latex(index=False, escape=False)
    save_raw_data_to_file(filename=file_path, data=averages_latex)


if __name__ == '__main__':
    # print(multiprocessing.cpu_count())
    parser = argparse.ArgumentParser(
        prog='AIk Distribution Calculator',
        description='Compute the AIk distribution of WPB functions',
    )
    parser.add_argument('-n', '--n_vars', help='number of variables', type=int, default=8)
    parser.add_argument('-O', '--sample_size', help='sample_size', type=int, default=10)
    parser.add_argument('-p', '--parallelize_by', type=lambda p: ParallelizationType(p),
                        default=ParallelizationType.SAMPLES.value,
                        help="Type of parallelization: Slices: slices, Samples: a or Sequencial: sequencial.")
    parser.add_argument('-kM', '--k_max', type=int, default=None, help="Maximum k - default None.")
    parser.add_argument('-km', '--k_min', type=int, default=0, help="Minimum k - default 0.")
    parser.add_argument('-pl', '--plot', action='store_true', help="Plot results")
    parser.add_argument('-alg', '--algorithm', type=lambda a: Algorithm(a),
                        default=Algorithm.IV.value, help='Algorithm to use: Alg 1 or Alg 3 - default 3.')
    args = parser.parse_args()
    _log.info(f"Arguments given: {args}")
    main(n=args.n_vars, k_max=args.k_max, k_min=args.k_min, sample_size=args.sample_size,
         parallelize_by=args.parallelize_by, plot=args.plot, algorithm=args.algorithm)
