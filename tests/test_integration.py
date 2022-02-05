"""Integration tests for functions counter."""
import operator
import pathlib

import pytest

from funk_lines.core import main, results

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

dummy_files = [
    ("hello_world_func_file", hello_world_func_file, 4, 1, 3),
    ("hello_world_simple_class", hello_world_simple_class, 5, 2, 3.5),
    ("hello_world_class", hello_world_class, 10, 3, 5),
    ("hello_closure", hello_closure, 7, 2, 4.5),
    ("no_funcs_file", no_funcs_file, 3, 0, None),
]


@pytest.mark.parametrize(
    "contents, expected_n_lines, expected_n_definitions, expected_avg_lines",
    zip(*list(zip(*dummy_files))[1:]),
    ids=list(zip(*dummy_files))[1],
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

    result = main.main(tmp_fp)

    assert result.total_lines == expected_n_lines
    assert result.nbr_definitions == expected_n_definitions
    assert result.lines_per_function == expected_avg_lines


def test_when_directory_is_empty(tmp_path: pathlib.Path) -> None:
    result = main.main(tmp_path)
    assert isinstance(result, results.EmptyResult)


def test_non_existing_file_raises_not_found_error() -> None:
    with pytest.raises(FileNotFoundError, match="foo"):
        main.main("foo")


def test_directory(tmp_path: pathlib.Path) -> None:
    total_lines = 0
    total_def = 0

    tmp_path.joinpath("empty").mkdir(parents=True)
    tmp_path.joinpath("not-python").write_text("foo")

    for file_name, content, n_lines, n_def, _ in dummy_files:
        file = tmp_path.joinpath(f"{file_name}/{file_name}.py")
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
        total_lines += n_lines
        total_def += n_def

    print(list(tmp_path.iterdir()))
    result = main.main(tmp_path)
    print(result)
    cumulative_n_lines = sum(map(operator.attrgetter("n_lines"), result.definitions))
    assert result.info() == (
        str(total_lines),
        str(total_def),
        f"{cumulative_n_lines / total_def:.2f}",
    )
