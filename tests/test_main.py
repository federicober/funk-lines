"""Test cases for the __main__ module."""
import pytest
from typer.testing import CliRunner

from funk_lines import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_version_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.app, "--version")
    assert result.exit_code == 0


def test_help_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.app, "--help")
    assert result.exit_code == 0


def test_without_commands_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.app)
    assert result.exit_code == 0
