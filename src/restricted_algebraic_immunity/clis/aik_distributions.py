import os
from pathlib import Path

import typer
import math

from restricted_algebraic_immunity.factory.AIk_distribution import AIkDistribution, DFKeys, \
    ParallelizationType, main, Algorithm
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
        algorithm: Algorithm = typer.Option(Algorithm.IV.value, help="algorithm to use."),
        plot: bool = typer.Option(False, help='Produce and save plot.')
):
    main(n=n, k_max=k_max, k_min=k_min, sample_size=sample_size, parallelize_by=parallelize_by, plot=plot, algorithm=algorithm)



