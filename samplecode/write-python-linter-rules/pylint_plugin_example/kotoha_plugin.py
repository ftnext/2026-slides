from astroid import nodes
from pylint.checkers import BaseChecker


class ArgumentListTypeHintChecker(BaseChecker):
    name = "kotoha-checker"
    priority = -1
    msgs = {
        "W9999": (
            "Avoid concrete list type in argument '%s'; use Sequence or Iterable instead",
            "avoid-list-arg-type",
            "Concrete list type in function argument type hints should be avoided.",
        ),
    }

    def visit_arguments(self, node: nodes.Arguments) -> None:
        for annotation in node.annotations:
            if (
                isinstance(annotation, nodes.Subscript)
                and isinstance(annotation.value, nodes.Name)
                and annotation.value.name == "list"
            ):
                self.add_message(
                    "avoid-list-arg-type",
                    node=annotation,
                    args=(annotation.value.name,),
                )


def register(linter):
    linter.register_checker(ArgumentListTypeHintChecker(linter))
