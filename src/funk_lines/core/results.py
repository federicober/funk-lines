"""File for the results class."""
import statistics
from typing import List, Optional, Sequence

from .ast_processors import StmtInfo


class Results:
    """Class for holding the results of an analysis.

    The Analyser classes return a Result object.
    """

    def __init__(self, total_lines: int, definitions: Sequence[StmtInfo]):
        """Result constructor.

        Args:
            total_lines: Total number of lines
            definitions: Sequence of functions and classes
        """
        self._total_lines: int = total_lines
        self._definitions: List[StmtInfo] = list(definitions)

    @property
    def total_lines(self) -> int:
        """Total number of lines."""
        return self._total_lines

    @property
    def nbr_definitions(self) -> int:
        """Total number of functions and classes."""
        return len(self._definitions)

    @property
    def definitions(self) -> List[StmtInfo]:
        """List of statement info objects for all functions and classes."""
        return self._definitions.copy()

    @property
    def lines_per_function(self) -> Optional[float]:
        """Mean number of lines per definition."""
        if self._definitions:
            return statistics.mean(def_.n_lines for def_ in self._definitions)
        return None

    def __add__(self, other: "Results") -> "Results":
        """Combines two results.

        Args:
            other: another Result object

        Returns:
            Combined results
        """
        return self.__class__(
            total_lines=self.total_lines + other.total_lines,
            definitions=self._definitions + other.definitions,
        )

    def info(self) -> tuple[str, str, str, str]:
        """Returns the information of the result in a printable manner"""
        return (
            "",
            str(self.total_lines),
            str(self.nbr_definitions),
            f"{self.lines_per_function:.2f}" if self.lines_per_function else "",
        )
