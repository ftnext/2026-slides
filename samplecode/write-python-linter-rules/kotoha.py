import ast


class ArgumentConcreteTypeHintChecker(ast.NodeVisitor):
    def visit_arg(self, node):
        annotation = node.annotation
        if annotation.value.id == "list":
            as_is = f"{node.arg}: {annotation.value.id}[{annotation.slice.id}]"
            print(f"Fix type hint `{as_is}` at {node.lineno}:{node.col_offset}")
        self.generic_visit(node)


source = """\
from collections.abc import Iterable


def plus_one_ng(numbers: list[int]) -> list[int]:
    return [n + 1 for n in numbers]


def plus_one_ok(numbers: Iterable[int]) -> list[int]:
    return [n + 1 for n in numbers]
"""
tree = ast.parse(source)
# print(ast.dump(tree, indent=2))
ArgumentConcreteTypeHintChecker().visit(tree)
