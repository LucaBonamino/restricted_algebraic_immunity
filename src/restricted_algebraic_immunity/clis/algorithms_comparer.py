import typer

from restricted_algebraic_immunity.factory.FMR_time_measurement import main as main_fmr_times
from restricted_algebraic_immunity.factory.IV_time_measurement import main as main_iv_times
from restricted_algebraic_immunity.factory.produce_time_comparison_plot import main as main_plot_comparison

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


@app.command('FRM-time-measurements')
def measure_iv_times(
        max_n: int = typer.Option(help="Maximum number of variables"),
        sample_size: int = typer.Option(help="Sample size")
):
    main_fmr_times(max_n, sample_size)


@app.command('IV-time-measurements')
def measure_frm_times(
        max_n: int = typer.Option(help="Maximum number of variables"),
        sample_size: int = typer.Option(help="Sample size")
):
    main_iv_times(max_n, sample_size)


@app.command('comparison-plot')
def ai_k_lt(
        sample_size: int = typer.Option(help="Sample size"),
        max_n: int = typer.Option(help="Maximum number of variables")
):
    main_plot_comparison(max_n=max_n, sample_size=sample_size)
