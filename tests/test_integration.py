"""Integration tests for functions counter."""
import pathlib

import pytest

from funk_lines.core import main

hello_world_func_file = """
def hello_world():
    print("Hello world")

hello_world()
"""

hello_world_simple_class = """
class HelloWorld:
    def __init__(self):
        print("Hello world")

HelloWorld()
"""


hello_world_class = """
class HelloWorld:
    _msg: str = "Hello world"

    def __init__(self):
        print(self._msg)

    def __str__(self) -> str:
        return _msg

HelloWorld()
"""

hello_closure = """
def make_hello(name: str):
    def hello():
        print("Hello", name)

    return hello

make_hello("Foo")()
"""

no_funcs_file = """
a = "Hello world"

print(a)
"""


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
    tmp_path: pathlib.Path,
    contents: str,
    expected_n_lines: int,
    expected_n_definitions: int,
    expected_avg_lines: float,
) -> None:
    tmp_fp = tmp_path / "foo.py"

    tmp_fp.write_text(contents)

    results = main.main(tmp_fp)

    assert results.total_lines == expected_n_lines
    assert results.nbr_definitions == expected_n_definitions
    assert results.lines_per_function == expected_avg_lines


def test_is_directory(tmp_path: pathlib.Path) -> None:
    with pytest.raises(NotImplementedError):
        main.main(tmp_path)


def test_non_existing_file_raises_not_found_error() -> None:
    with pytest.raises(FileNotFoundError, match="foo"):
        main.main("foo")
