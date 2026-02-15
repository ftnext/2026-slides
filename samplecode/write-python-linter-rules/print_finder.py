import ast


class PrintFinder(ast.NodeVisitor):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            args = [arg.value for arg in node.args]
            print(f"Found print at line {node.lineno}, args {args}")
        self.generic_visit(node)


source = """\
print("静岡")
len("静岡")
print("最高")
"""
tree = ast.parse(source)
# print(ast.dump(tree, indent=2))
PrintFinder().visit(tree)
