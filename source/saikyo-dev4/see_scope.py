import symtable

src1 = """\
import json

def f():
    data = json.loads("{}")
    return data
"""

top = symtable.symtable(src1, "example.py", "exec")
func = next(child for child in top.get_children() if child.get_name() == "f")

print("src1")
for name in sorted(func.get_identifiers()):
    symbol = func.lookup(name)
    print(
        f"{name} local={symbol.is_local()} global={symbol.is_global()} "
        f"imported={symbol.is_imported()} referenced={symbol.is_referenced()}"
    )
print()

src2 = """\
import json

def f():
    data = json.loads("{}")
    import json
    return data
"""

top = symtable.symtable(src2, "example.py", "exec")
func = next(child for child in top.get_children() if child.get_name() == "f")

print("src2")
for name in sorted(func.get_identifiers()):
    symbol = func.lookup(name)
    print(
        f"{name} local={symbol.is_local()} global={symbol.is_global()} "
        f"imported={symbol.is_imported()} referenced={symbol.is_referenced()}"
    )
