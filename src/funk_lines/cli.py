"""Command-line interface."""
import typer

from . import __version__

app: typer.Typer = typer.Typer(name="Funk Lines CLI")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"Funk Lines, {__version__}")
        raise typer.Exit(code=0)


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, help="Show version and exit.", is_eager=True
    )
) -> None:
    """Funk Lines CLI."""
    _ = version  # pragma: no cover
