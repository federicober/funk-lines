"""Code of the main entrypoint for the application"""
import os
import pathlib

from . import results
from .analysers import file_analyser


def main(path: os.PathLike[str] | str) -> results.Results:
    """Runs funk_lines against a file or directory"""
    path_ = pathlib.Path(path)

    if not path_.exists():
        raise FileNotFoundError(str(path))

    if not path_.is_file():
        raise NotImplementedError()
    result = file_analyser.FileAnalyser(path).analyse()

    return result
