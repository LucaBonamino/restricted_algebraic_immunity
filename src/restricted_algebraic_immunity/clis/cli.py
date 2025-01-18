import typer

from restricted_algebraic_immunity.clis.ai_distributions import app as distributions_app
from restricted_algebraic_immunity.clis.aik_of_published_functions import app as published_functions
from restricted_algebraic_immunity.clis.algorithms_comparer import app as algorithms_comparison

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)
app.add_typer(distributions_app, name='distributions')
app.add_typer(published_functions, name='functions')
app.add_typer(algorithms_comparison, name='algs-comparison')