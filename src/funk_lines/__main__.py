"""Entrypoint of the python package."""
from .cli import app

__all__ = ["app"]

if __name__ == "__main__":
    app()  # pragma: no cover
