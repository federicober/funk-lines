"""Test cases for the __main__ module."""
import pathlib
import traceback
from unittest import mock

import pkg_resources
import pytest
from _pytest.monkeypatch import MonkeyPatch
from click.testing import Result
from typer.testing import CliRunner

from funk_lines import __main__


def assert_success(result: "Result") -> None:
    print(result.output)
    traceback.print_exception(result.exception)  # type: ignore[arg-type]
    assert result.exit_code == 0


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_version_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.app, "--version")
    assert_success(result)

    version = pkg_resources.get_distribution("funk_lines").version
    assert f"Funk Lines {version}" in result.output


def test_help_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.app, "--help")
    assert_success(result)


def test_call_executes_main(
    monkeypatch: MonkeyPatch, tmp_path: pathlib.Path, runner: CliRunner
) -> None:
    main_mock = mock.MagicMock()
    table_mock = mock.MagicMock()
    console_mock = mock.MagicMock()
    monkeypatch.setattr("funk_lines.core.main.main", main_mock)
    monkeypatch.setattr("rich.table.Table", table_mock)
    monkeypatch.setattr("rich.console.Console", console_mock)

    info = ["foo"] * 4
    main_mock.return_value.info.return_value = info

    result = runner.invoke(__main__.app, str(tmp_path))
    assert_success(result)

    print(main_mock.mock_calls)
    main_mock.assert_called_once_with(tmp_path)
    print(table_mock.mock_calls)
    table_mock.return_value.add_row.assert_any_call(*info)
    print(console_mock.mock_calls)
    console_mock.return_value.print.assert_any_call(table_mock.return_value)
