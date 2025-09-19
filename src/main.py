import typer
import cloud
import modules

cli = typer.Typer()
cli.add_typer(modules.cli)
cli.add_typer(cloud.cli)

if __name__ == "__main__":
    cli()