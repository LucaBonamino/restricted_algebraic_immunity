import os
from pathlib import Path

import typer
import math

from restricted_algebraic_immunity.factory.AIk_distribution import AIkDistribution, DFKeys, \
    ParallelizationType, main, Algorithm
from restricted_algebraic_immunity.factory.plotter_utils import from_latex_to_dataframe, \
    from_dataframe_to_dict_of_dataframes
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
        parallelize_by: ParallelizationType = typer.Option(ParallelizationType.SLICES.value,
                                                           help='Type of parallelization.'),
        algorithm: Algorithm = typer.Option(help="algorithm to use."),
        plot: bool = typer.Option(False, help='Produce and save plot.')
):
    main(n=n, k_max=k_max, k_min=k_min, sample_size=sample_size, parallelize_by=parallelize_by, plot=plot, algorithm=algorithm)


@app.command('plot-distribution')
def plot_dist(
        dist_filename: str = typer.Argument(help="Filename containing the AIk distribution to plot"),
        average_filename: str = typer.Argument(help="Filename containing the AIk averages to plot"),
        parallelize_by: ParallelizationType = typer.Option(ParallelizationType.SLICES.value,
                                                           help='Type of parallelization.'),
        sample_size: int = typer.Option(default=16, help="Sample size"),
        n: int = typer.Option(16)
):
    df_dist = from_latex_to_dataframe(filename=Path(dist_filename))
    print(df_dist)
    dict_df = from_dataframe_to_dict_of_dataframes(data_frame=df_dist, key_label=DFKeys.K.value,
                                                   other_labels=[DFKeys.AIK.value, DFKeys.AIK_DIST.value])
    AIkDistribution.plot_prob_distribution(prob_vals=dict_df, sample_size=sample_size,
                                           parallelization_type=parallelize_by.value,
                                           m=int(math.log(n, 2)), n=n)

    df_averages = from_latex_to_dataframe(filename=Path(average_filename))
    AIkDistribution.plot_aik_average(average_dataframe=df_averages, sample_size=sample_size,
                                     parallelization_type=parallelize_by.value,
                                     m=int(math.log(n, 2)), n=n)
