import symtable

src_before = """\
import json

def f():
    data = json.loads("{}")
    return data
"""

top = symtable.symtable(src_before, "example.py", "exec")
func = next(child for child in top.get_children() if child.get_name() == "f")

print("src1")
for name in sorted(func.get_identifiers()):
    symbol = func.lookup(name)
    print(
        f"{name} local={symbol.is_local()} global={symbol.is_global()} "
        f"imported={symbol.is_imported()} referenced={symbol.is_referenced()}"
    )
print()

src_ref = """\
import json

def f():
    import json
    data = json.loads("{}")
    return data
"""

top = symtable.symtable(src_ref, "example.py", "exec")
func = next(child for child in top.get_children() if child.get_name() == "f")

print("src_ref")
for name in sorted(func.get_identifiers()):
    symbol = func.lookup(name)
    print(
        f"{name} local={symbol.is_local()} global={symbol.is_global()} "
        f"imported={symbol.is_imported()} referenced={symbol.is_referenced()}"
    )
print()

src_after = """\
import json

def f():
    data = json.loads("{}")
    import json
    return data
"""

top = symtable.symtable(src_after, "example.py", "exec")
func = next(child for child in top.get_children() if child.get_name() == "f")

print("src2")
for name in sorted(func.get_identifiers()):
    symbol = func.lookup(name)
    print(
        f"{name} local={symbol.is_local()} global={symbol.is_global()} "
        f"imported={symbol.is_imported()} referenced={symbol.is_referenced()}"
    )
