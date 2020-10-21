"""Integration tests for functions counter."""
import pathlib
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from os import PathLike

    StrPathLike = PathLike[str]

hello_world_func_file = """
def hello_world():
    print("Hello world")

hello_world()
""".strip(
    "\n"
)

hello_world_simple_class = """
class HelloWorld:
    def __init__(self):
        print("Hello world")

HelloWorld()
""".strip(
    "\n"
)


hello_world_class = """
class HelloWorld:
    _msg: str = "Hello world"

    def __init__(self):
        print(self._msg)

    def __str__(self) -> str:
        return _msg

HelloWorld()
""".strip(
    "\n"
)

hello_closure = """
def make_hello(name: str):
    def hello():
        print("Hello", name)

    return hello

make_hello("Foo")()
""".strip(
    "\n"
)

no_funcs_file = """
a = "Hello world"

print(a)
""".strip(
    "\n"
)


@pytest.mark.parametrize(
    "contents, expected_n_lines, expected_n_definitions, expected_avg_lines",
    [
        (hello_world_func_file, 4, 1, 3),
        (hello_world_simple_class, 5, 2, 3.5),
        (hello_world_class, 10, 3, 5),
        (hello_closure, 7, 2, 4.5),
        (no_funcs_file, 3, 0, None),
    ],
    ids=[
        "hello_world_func",
        "hello_world_simple_class",
        "hello_world_class",
        "hello_closure",
        "no_funcs_file",
    ],
)
def test_file_analyser(
    tmpdir: "StrPathLike",
    contents: str,
    expected_n_lines: int,
    expected_n_definitions: int,
    expected_avg_lines: float,
) -> None:
    """Tests the results of a file analyser.

    Args:
        contents: Source code to be analysed
        expected_n_lines: Expected total number of lines
        expected_n_definitions: Expected total number of definitions
        expected_avg_lines: Expected average number of lines per definition
        tmpdir: temporary directory
    """
    from funk_lines.core.analysers import file_analyser

    tmp_fp = pathlib.Path(tmpdir) / "foo.py"

    tmp_fp.write_text(contents)

    analyser = file_analyser.FileAnalyser(tmp_fp)

    results = analyser.analyse()
    assert results.total_lines == expected_n_lines
    assert results.nbr_definitions == expected_n_definitions
    assert results.lines_per_function == expected_avg_lines
