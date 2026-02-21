# Write Python linter rules

## Python

### basic

```
% python kotoha.py
```

### flake8

```
% cd flake8_plugin_example
% python -m venv .venv
% source .venv/bin/activate
% python -m pip install .
% flake8 ../lint-targets/use_iterable.py
```

### pylint

```
% cd pylint_plugin_example
% PYTHONPATH=. uvx pylint --load_plugins kotoha_plugin --disable=all --enable=avoid-list-arg-type ../lint-targets/use_iterable.py
```

## Rust

### ast-grep

```
% uvx --from ast-grep-cli ast-grep scan --rule kotoha.yaml lint-targets/use_iterable.py
```

### tree-sitter

https://dcreager.net/2021/06/getting-started-with-tree-sitter/#Installing-tree-sitter

```
% tree-sitter query kotoha.scm lint-targets/use_iterable.py 
```

### Write Rust (with RustPython/Parser)

See https://github.com/ftnext/command-line-rust-book/tree/main/self-taught/hello-python-ast
