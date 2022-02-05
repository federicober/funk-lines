import pytest

from funk_lines.core.analysers import dir_analyser


def test_dir_analyser_with_not_directory_raises_error() -> None:
    with pytest.raises(NotADirectoryError, match="bar"):
        dir_analyser.DirectoryAnalyser("bar").analyse()
