"""Test cases for the __main__ module."""
import pathlib
import traceback
from unittest import mock

import pkg_resources
import pytest
import rich
from _pytest.monkeypatch import MonkeyPatch
from click.testing import Result
from typer.testing import CliRunner

from funk_lines import __main__
from funk_lines.core import results


def handle_result(result: "Result") -> None:
    print(result.output)
    traceback.print_exception(result.exception)  # type: ignore[arg-type]


def assert_success(result: "Result") -> None:
    handle_result(result)
    assert result.exit_code == 0


def assert_failed(result: "Result") -> None:
    handle_result(result)
    assert result.exit_code == 1


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


@pytest.fixture()
def mock_externals(
    monkeypatch: MonkeyPatch,
) -> tuple[mock.MagicMock, mock.MagicMock, mock.MagicMock]:
    main_mock = mock.MagicMock()
    table_mock = mock.MagicMock()
    console_mock = mock.MagicMock()
    monkeypatch.setattr("funk_lines.core.main.main", main_mock)
    monkeypatch.setattr("rich.table.Table", table_mock)
    monkeypatch.setattr("funk_lines.cli.console", console_mock)
    console_mock.print.side_effect = rich.console.Console().print
    return main_mock, table_mock, console_mock


def get_result_mock() -> mock.Mock:
    mck = mock.Mock(info=mock.MagicMock(return_value=["foo"] * 3), children=[])
    mck.name = "name"
    return mck


def test_call_executes_main(
    tmp_path: pathlib.Path,
    runner: CliRunner,
    mock_externals: tuple[mock.MagicMock, mock.MagicMock, mock.MagicMock],
) -> None:
    main_mock, table_mock, console_mock = mock_externals

    main_mock.return_value = get_result_mock()
    main_mock.return_value.children = [get_result_mock()]
    result = runner.invoke(__main__.app, str(tmp_path))
    assert_success(result)

    print(main_mock.mock_calls)
    main_mock.assert_called_once_with(tmp_path)
    print(table_mock.mock_calls)
    table_mock.return_value.add_row.assert_any_call("name", *["foo"] * 3)
    table_mock.return_value.add_row.assert_any_call("    name", *["foo"] * 3)
    print(console_mock.mock_calls)
    console_mock.print.assert_any_call(table_mock.return_value)


def test_call_executes_main_exists_when_empty_dir(
    tmp_path: pathlib.Path,
    runner: CliRunner,
    mock_externals: tuple[mock.MagicMock, mock.MagicMock, mock.MagicMock],
) -> None:
    main_mock, table_mock, console_mock = mock_externals
    main_mock.return_value = results.EmptyResult(name="Empty")

    result = runner.invoke(__main__.app, str(tmp_path))
    assert_failed(result)

    assert str(tmp_path) in result.output
    assert "python file" in result.output.lower()
