import enum
import os
from pathlib import Path

import typer
import math

from restricted_algebraic_immunity.factory.AIk_distribution import AIkDistribution, save_raw_data_to_file, DFKeys
from restricted_algebraic_immunity.factory.plotter_utils import from_latex_to_dataframe, \
    from_dataframe_to_dict_of_dataframes
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class ParallelizationType(enum.Enum):
    SLICES = 'slices'
    SAMPLES = 'a'
    SEQUENCIAL = 'sequencial'


def main(n: int, k_max: int, k_min: int, parallelize_by: ParallelizationType, sample_size: int, plot: bool):
    slice_k = list(range(n + 1))
    if k_max is not None:
        if k_max != k_min:
            slice_k = list(range(k_min, k_max + 1))
        else:
            slice_k = [k_min]

    print(slice_k)
    m_log = int(math.log(n, 2))
    if parallelize_by == ParallelizationType.SLICES:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel(m=m_log, n=n, s=sample_size,
                                                                       k_range=slice_k)
    elif parallelize_by == ParallelizationType.SAMPLES:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=n, s=sample_size,
                                                                           k_range=slice_k)
    else:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_non_parallel(m=m_log, n=n,
                                                                                    s=sample_size, k_range=slice_k)
        # dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=args.n_vars, s=args.sample_size)
    times_latex = times_df.to_latex(index=False, escape=False)
    dire = Path(
        os.path.join(SCRIPT_DIR, f"../factory/results/IV/AIk_distributions/n_{n}"))
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
    # AIkDistribution.plot_dist(distribution_data=(None, None), sample_size=args.sample_size, n=args.n_vars,
    #                           save=True)
    file_path = dire / f"distribution_n_{n}_sample_{sample_size}_{parallelize_by.value}_{k_min}_{k_max}.txt"
    save_raw_data_to_file(filename=file_path, data=dist_latex)

    file_path = dire / f"distribution_n_{n}_sample_{sample_size}_{parallelize_by.value}_{k_min}_{k_max}_averages.txt"
    averages_latex = df_averages.to_latex(index=False, escape=False)
    save_raw_data_to_file(filename=file_path, data=averages_latex)


@app.command('AIk-distribution')
def calculate_distribution(
        n: int = typer.Option(16, help="Number of variables."),
        sample_size: int = typer.Option(2, help="Sample size."),
        k_min: int = typer.Option(0, help='Minimum value of k.'),
        k_max: int = typer.Option(None, help='Maximum value of k.'),
        parallelize_by: ParallelizationType = typer.Option(ParallelizationType.SLICES.value,
                                                           help='Type of parallelization.'),
        plot: bool = typer.Option(False, help='Produce and save plot.')
):
    main(n=n, k_max=k_max, k_min=k_min, sample_size=sample_size, parallelize_by=parallelize_by, plot=plot)


@app.command('plot-distribution')
def plot_dist(
        dist_filename: str = typer.Argument(help="Filename containing the AIk distribution to plot"),
        average_filename: str = typer.Argument(help="Filename containing the AIk averages to plot"),
        sample_size: int = typer.Option(default=16, help="Sample size"),
        n: int = typer.Option(16)
):
    df_dist = from_latex_to_dataframe(filename=Path(dist_filename))
    print(df_dist)
    dict_df = from_dataframe_to_dict_of_dataframes(data_frame=df_dist, key_label=DFKeys.K.value,
                                                   other_labels=[DFKeys.AIK.value, DFKeys.AIK_DIST.value])
    AIkDistribution.plot_prob_distribution(prob_vals=dict_df, sample_size=sample_size, parallelization_type="a",
                                           m=int(math.log(n, 2)), n=n)

    df_averages = from_latex_to_dataframe(filename=Path(average_filename))
    AIkDistribution.plot_aik_average(average_dataframe=df_averages, sample_size=sample_size, parallelization_type="a",
                                     m=int(math.log(n, 2)), n=n)
