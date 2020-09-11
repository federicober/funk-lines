"""Command-line interface."""
import pathlib

import rich
import rich.console
import rich.table
import typer

app: typer.Typer = typer.Typer(name="Funk Lines CLI")


def _version_callback(value: bool) -> None:
    if value:
        import pkg_resources

        version = pkg_resources.get_distribution(__name__.split(".", maxsplit=1)[0]).version

        rich.print(f"Funk Lines [cyan]{version}[/cyan]")
        raise typer.Exit(code=0)


@app.command()
def callback(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, help="Show version and exit.", is_eager=True
    ),
    src: pathlib.Path = typer.Argument(..., dir_okay=True, file_okay=True, exists=True),
) -> None:
    """Funk Lines CLI."""
    from .core import main

    _ = version

    result = main.main(src)

    table = rich.table.Table(
        rich.table.Column("Name", justify="right", style="cyan", no_wrap=True),
        rich.table.Column("Lines", justify="left", style="magenta"),
        rich.table.Column("Functions", justify="left", style="magenta"),
        rich.table.Column("Lines/Func", justify="left", style="green"),
    )

    table.add_row(*result.info())

    console = rich.console.Console()
    console.print(table)
