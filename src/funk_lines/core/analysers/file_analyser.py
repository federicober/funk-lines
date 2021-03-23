"""Class for analysing a single python file."""
import ast
import pathlib
from os import PathLike
from typing import TYPE_CHECKING, Union

from funk_lines.core import results

from ..ast_processors import base as _base_processor
from ..ast_processors import function_processor

if TYPE_CHECKING:
    PathLikeStr = PathLike[str]
else:
    PathLikeStr = PathLike


class FileAnalyser:
    """Analyser for a single Python file."""

    def __init__(self, file_path: Union[str, "PathLikeStr"]):
        """Constructor for FileAnalyser.

        Args:
            file_path: Location to the file to be analysed
        """
        self._file_path: pathlib.Path = pathlib.Path(str(file_path))
        self._contents: str = self._file_path.read_text()
        self._node: "ast.Module" = ast.parse(self._contents)
        eof = _base_processor.EOF(self.count_lines() + 1)
        self._definitions = function_processor.get_definitions(self._node, next_node=eof)

    def analyse(self) -> results.Results:
        """Extracts the results from the analysed object.

        Returns:
            Results object
        """
        return results.Results(total_lines=self.count_lines(), definitions=self._definitions)

    def count_lines(self) -> int:
        """Counts the total number of lines.

        Returns:
            integer
        """
        return len(self._contents.split("\n"))
