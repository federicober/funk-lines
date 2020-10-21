"""Processes for functions and classes in AST trees."""
import ast
import collections
import functools
import itertools
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Tuple
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

from .base import AstDefinitions
from .base import StmtInfo

if TYPE_CHECKING:
    AstInfoSequence = collections.abc.Collection[StmtInfo]
else:
    AstInfoSequence = collections.abc.Collection

X = TypeVar("X")


def _pairwise(iterable: Iterable[X], ending: X) -> Iterator[Tuple[X, X]]:
    """Iterates through an object pairwise.

    Examples:
        s -> (s_0,s_1), (s_1,s_2), (s_2, s_3), ..., (s_last, ending)

    Args:
        iterable: Original iterable
        ending: Last value to after at ending

    Returns:
        Iterator of tuples of pairs
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.zip_longest(a, b, fillvalue=ending)


def is_definition(node: Any) -> bool:
    """Returns True if the object is a definition ast node.

    Args:
        node: object to be evaluated

    Returns:
        True if node is a Definition
    """
    return any(isinstance(node, t) for t in AstDefinitions)


def get_definitions(
    current_node: Union[ast.stmt, ast.Module], next_node: ast.stmt,
) -> "List[StmtInfo]":
    """Constructs a InfoSequence object from an AST node.

    Args:
        current_node: AST Node from which to generate the InfoSequence
        next_node: Next AST node, useful for extracting additional information

    Returns:
        List of StmtInfo
    """
    current_node_info: "List[StmtInfo]" = []

    if is_definition(current_node) and not isinstance(current_node, ast.Module):
        current_node_info = [StmtInfo(current_node, next_node=next_node)]

    if hasattr(current_node, "body"):
        _body: List[ast.stmt] = current_node.body  # type: ignore
        return current_node_info + functools.reduce(
            list.__add__, itertools.starmap(get_definitions, _pairwise(_body, ending=next_node))
        )

    return current_node_info
