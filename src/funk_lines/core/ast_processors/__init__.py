"""Core package for processing an AST tree."""
from .base import EOF
from .base import StmtInfo
from .function_processor import get_definitions

__all__ = ["EOF", "StmtInfo", "get_definitions"]
