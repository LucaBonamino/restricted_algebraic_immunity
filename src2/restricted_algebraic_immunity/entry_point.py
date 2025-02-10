from restricted_algebraic_immunity.clis import cli


def main():
    cli.app(prog_name='restrictedAI')
    cli.app.add_typer()
