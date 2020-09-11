"""Class for analysing a single python file."""
import ast
import pathlib
from os import PathLike

from funk_lines.core import results

from ..ast_processors import base as _base_processor
from ..ast_processors import function_processor


class FileAnalyser:
    """Analyser for a single Python file."""

    def __init__(self, file_path: str | PathLike[str]):
        """Constructor for FileAnalyser.

        Args:
            file_path: Location to the file to be analysed
        """
        self._file_path: pathlib.Path = pathlib.Path(str(file_path))
        self._contents: str = self._file_path.read_text("utf-8").strip(
            "\n"
        )  # remove new lines because not relevant

    def analyse(self) -> results.Results:
        """Extracts the results from the analysed object.

        Returns:
            Results object
        """
        base_ast_node: "ast.Module" = ast.parse(self._contents)
        eof = _base_processor.EOF(self.count_lines() + 1)
        definitions = function_processor.get_definitions(base_ast_node, next_node=eof)
        return results.Results(total_lines=self.count_lines(), definitions=definitions)

    def count_lines(self) -> int:
        """Counts the total number of lines.

        Returns:
            integer
        """
        return len(self._contents.split("\n"))
