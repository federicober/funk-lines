"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Funk Lines."""


if __name__ == "__main__":
    main(prog_name="funk-lines")  # pragma: no cover
