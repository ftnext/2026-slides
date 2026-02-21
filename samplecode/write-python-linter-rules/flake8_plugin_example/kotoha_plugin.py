import ast
from collections.abc import Generator
from typing import Any, Type


class ArgumentListTypeHintChecker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[tuple[int, int, str]] = []

    def visit_arg(self, node):
        annotation = node.annotation
        if isinstance(annotation, ast.Subscript) and annotation.value.id == "list":
            as_is = f"{node.arg}: {annotation.value.id}[{annotation.slice.id}]"
            self.errors.append(
                (node.lineno, node.col_offset, f"KTH001 Fix type hint `{as_is}`")
            )
        self.generic_visit(node)


class Flake8KotohaPlugin:
    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, Type[Any]], None, None]:
        checker = ArgumentListTypeHintChecker()
        checker.visit(self._tree)

        for lineno, col_offset, message in checker.errors:
            yield (lineno, col_offset, message, type(self))
