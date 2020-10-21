"""Tests for the Result class."""
from typing import List
from unittest import mock


def test_results_add() -> None:
    """Test the results add method."""
    from funk_lines.core import results
    from funk_lines.core.ast_processors import StmtInfo

    def _mock_definitions(*args: int) -> List["StmtInfo"]:
        result: List[StmtInfo] = []
        for i in args:
            mock_ = mock.NonCallableMock()  # type: StmtInfo
            mock_._n_lines = i
            mock_.__class__ = StmtInfo
            result.append(mock_)
        return result

    first = results.Results(3, _mock_definitions(3, 2))
    second = results.Results(4, _mock_definitions(2))
    combined = first + second
    assert combined.total_lines == 7
    assert combined.nbr_definitions == 3
