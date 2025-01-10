import typer

from restricted_algebraic_immunity.factory.AIk_of_published_functions import tl, dm_24, zn_23

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


@app.command('ZS23')
def ai_k_of_zs_24(
        n: int = typer.Option(16, help="Number of variables"),
):
    print(zn_23(n))


@app.command('DM24')
def ai_k_of_dm_24(
        n: int = typer.Option(16, help="Number of variables"),
):
   print(dm_24(n))


@app.command('TL19')
def ai_k_LT(
        n: int = typer.Option(16, help="Number of variables"),
):
    print(tl(n))
