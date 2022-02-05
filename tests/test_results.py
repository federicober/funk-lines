"""Tests for the Result class."""
from typing import List
from unittest import mock

from funk_lines.core import results
from funk_lines.core.ast_processors import StmtInfo


def test_results_add() -> None:
    """Test the results add method."""

    def _mock_definitions(*args: int) -> List["StmtInfo"]:
        result: List[StmtInfo] = []
        for i in args:
            mock_ = mock.NonCallableMock()  # type: StmtInfo
            mock_.n_lines = i  # type: ignore[misc]
            mock_.__class__ = StmtInfo
            result.append(mock_)
        return result

    first = results.Result(3, _mock_definitions(3, 2), name="1")
    second = results.Result(4, _mock_definitions(2), name="2")
    combined = first + second
    assert combined.total_lines == 7
    assert combined.nbr_definitions == 3
    assert combined.info() == ("7", "3", "2.33")


def test_properties_of_empty_result() -> None:
    empty_result = results.EmptyResult(name="Empty")

    assert not empty_result.definitions
    assert empty_result.nbr_definitions == 0
    assert empty_result.total_lines == 0
    assert empty_result.lines_per_function is None
    assert empty_result.info() == ("0", "0", "")
    assert str(empty_result) == "Result from Empty"
    assert repr(empty_result) == "EmptyResult(Empty)"

    second_empty_result = results.EmptyResult(name="Empty2")
    assert empty_result + second_empty_result is second_empty_result
