import typer

from restricted_algebraic_immunity.clis.ai_distributions import app as distributions_app

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)
app.add_typer(distributions_app, name='distributions')