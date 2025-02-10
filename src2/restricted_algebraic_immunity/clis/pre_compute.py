import os

import typer

from restricted_algebraic_immunity.full_reed_muller.pre_compute import pre_compute_by_n_vars
from restricted_algebraic_immunity.utils.logging import get_logger

_log = get_logger(__name__)

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))




@app.command('pre-compute-by-n')
def pre_compute_by_n(
        n: int = typer.Option(16, help="Number of variables."),
):
    pre_compute_by_n_vars(n=n)