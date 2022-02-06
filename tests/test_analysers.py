import pathlib
from unittest import mock

import pytest
from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from funk_lines.core.analysers import dir_analyser, file_analyser


def test_dir_analyser_with_not_directory_raises_error() -> None:
    with pytest.raises(NotADirectoryError, match="bar"):
        dir_analyser.DirectoryAnalyser("bar").analyse()


def test_analyser_logs_critical_error_when_exception(
    tmp_path: pathlib.Path, monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    python_file = tmp_path / "foo.py"
    python_file.write_text("print('foo')")

    analyser = file_analyser.FileAnalyser(python_file)
    monkeypatch.setattr(analyser, "_analyse", mock.MagicMock(side_effect=RuntimeError))

    with pytest.raises(RuntimeError):
        analyser.analyse()

    assert f"Exception from {python_file}" in caplog.messages
