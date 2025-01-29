import typer

from restricted_algebraic_immunity.factory.AIk_of_published_functions import tl, dm_24, zn_23, cmr

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


@app.command('ZS23')
def ai_k_of_zs_24(
        n: int = typer.Option(16, help="Number of variables"),
        check: bool = typer.Option(False, help='Check if the function is WPB')
):
    print(zn_23(n), check)


@app.command('DM24')
def ai_k_of_dm_24(
        n: int = typer.Option(16, help="Number of variables"),
        check: bool = typer.Option(False, help='Check if the function is WPB')
):
    print(dm_24(n), check)


@app.command('TL19')
def ai_k_lt(
        n: int = typer.Option(16, help="Number of variables"),
        check: bool = typer.Option(False, help='Check if the function is WPB')
):
    print(tl(n), check)


@app.command('CMR')
def ai_k_lt(
        n: int = typer.Option(16, help="Number of variables"),
        check: bool = typer.Option(False, help='Check if the function is WPB')
):
    print(cmr(n, check))
