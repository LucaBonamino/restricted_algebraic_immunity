import os
from pathlib import Path

import typer
import math

from restricted_algebraic_immunity.factory.AIk_distribution import AIkDistribution, save_raw_data_to_file
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.command('AIk-distribution')
def calculate_distribution(
        n: int = typer.Option(16, help="Number of variables."),
        sample_size: int = typer.Option(2, help="Sample size."),
        k_min: int = typer.Option(0, help='Minimum value of k.'),
        k_max: int = typer.Option(None, help='Maximum value of k.'),
        parallelize_by: str = typer.Option('slices', help='Type of parallelization.'),
        plot: bool = typer.Option(False, help='Produce and save plot.')
):
    slice_k = list(range(n + 1))
    if k_max is not None:
        if k_max != k_min:
            slice_k = list(range(k_min, k_max + 1))
        else:
            slice_k = [k_min]

    print(slice_k)
    m_log = int(math.log(n, 2))
    if parallelize_by == 'slice':
        dist_df, times_df, df_averages = AIkDistribution.func_parallel(m=m_log, n=n, s=sample_size,
                                                                       k_range=slice_k)
    elif parallelize_by == 'a':
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=n, s=sample_size,
                                                                           k_range=slice_k)
    else:
        dist_df, times_df, df_averages = AIkDistribution.func_parallel_non_parallel(m=m_log, n=n,
                                                                                    s=sample_size, k_range=slice_k)
        # dist_df, times_df, df_averages = AIkDistribution.func_parallel_seq(m=m_log, n=args.n_vars, s=args.sample_size)
    times_latex = times_df.to_latex(index=False, escape=False)

    file_path = Path(
        os.path.join(SCRIPT_DIR,
                     f"../factory/results/IV/AIk_distributions/times_n_{n}_sample_{sample_size}_{parallelize_by}_{k_min}_{k_max}.txt"))
    save_raw_data_to_file(filename=file_path, data=times_latex)
    print(dist_df)
    dist_latex = dist_df[1].to_latex(index=False, escape=False)
    if plot is True:
        AIkDistribution.plot_dist(distribution_data=(df_averages, dist_df[0]), sample_size=sample_size,
                                  n=n,
                                  save=True, parallelization_type=parallelize_by, max_k=str(k_max),
                                  min_k=str(k_min))
    # AIkDistribution.plot_dist(distribution_data=(None, None), sample_size=args.sample_size, n=args.n_vars,
    #                          save=True)
    file_path = Path(
        os.path.join(SCRIPT_DIR,
                     f"../factory/results/IV/AIk_distributions/distribution_n_{n}_sample_{sample_size}_{parallelize_by}_{k_min}_{k_max}.txt"))
    save_raw_data_to_file(filename=file_path, data=dist_latex)

    file_path = Path(
        os.path.join(SCRIPT_DIR,
                     f"../factory/results/IV/AIk_distributions/distribution_n_{n}_sample_{sample_size}_{parallelize_by}_{k_min}_{k_max}_averages.txt"))
    averages_latex = df_averages.to_latex(index=False, escape=False)
    save_raw_data_to_file(filename=file_path, data=averages_latex)
