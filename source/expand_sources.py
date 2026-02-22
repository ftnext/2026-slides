from __future__ import annotations

import re
from pathlib import Path

INCLUDE_RE = re.compile(r"^(\s*)\.\.\s+include::\s+(.+?)\s*$")
OPT_RE = re.compile(r"^\s*:(start-line|end-line|start-after|end-before):\s*(.*?)\s*$")


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (
        s.startswith("'") and s.endswith("'")
    ):
        return s[1:-1]
    return s


def _resolve_include_path(arg: str, current_file: Path, srcdir: Path) -> Path:
    p = _strip_quotes(arg)
    if p.startswith("/"):
        return (srcdir / p[1:]).resolve()
    return (current_file.parent / p).resolve()


def _apply_include_options(text: str, opts: dict[str, str]) -> str:
    lines = text.splitlines(keepends=True)

    if "start-line" in opts:
        try:
            start = int(opts["start-line"])
            lines = lines[start:]
        except ValueError:
            pass

    if "end-line" in opts:
        try:
            end = int(opts["end-line"])
            lines = lines[:end]
        except ValueError:
            pass

    text2 = "".join(lines)

    if "start-after" in opts:
        marker = opts["start-after"]
        i = text2.find(marker)
        if i != -1:
            text2 = text2[i + len(marker) :]

    if "end-before" in opts:
        marker = opts["end-before"]
        i = text2.find(marker)
        if i != -1:
            text2 = text2[:i]

    return text2


def _collect_include_options(lines: list[str], i: int) -> tuple[dict[str, str], int]:
    opts: dict[str, str] = {}
    j = i + 1
    while j < len(lines):
        line = lines[j]
        if line.strip() == "":
            j += 1
            continue
        if not line.startswith((" ", "\t")):
            break
        m = OPT_RE.match(line)
        if m:
            opts[m.group(1)] = m.group(2)
        j += 1
    return opts, j


def _expand_includes(
    text: str,
    current_file: Path,
    srcdir: Path,
    stack: set[Path],
) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        m = INCLUDE_RE.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        indent, target = m.group(1), m.group(2)
        opts, next_i = _collect_include_options(lines, i)

        inc_path = _resolve_include_path(target, current_file, srcdir)
        if inc_path in stack or not inc_path.exists():
            out.append(line)
            i = next_i
            continue

        raw = inc_path.read_text(encoding="utf-8")
        raw = _apply_include_options(raw, opts)
        expanded = _expand_includes(raw, inc_path, srcdir, stack | {inc_path})

        if indent:
            expanded = "".join(
                (indent + l if l.strip() else l)
                for l in expanded.splitlines(keepends=True)
            )
        out.append(expanded)
        i = next_i

    return "".join(out)


def _sourcename(app, docname: str) -> str:
    source_suffix = str(app.env.doc2path(docname, False))[len(docname) :]
    name = docname + source_suffix
    if source_suffix != app.config.html_sourcelink_suffix:
        name += app.config.html_sourcelink_suffix
    return name


def write_expanded_sources(app, exception) -> None:
    if exception:
        return
    if app.builder.format != "html":
        return
    if not app.config.html_copy_source:
        return

    srcdir = Path(app.srcdir).resolve()
    out_sources = Path(app.outdir) / "_sources"
    out_sources.mkdir(parents=True, exist_ok=True)

    for docname in app.env.found_docs:
        src = Path(app.env.doc2path(docname)).resolve()
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        expanded = _expand_includes(text, src, srcdir, {src})

        dest = out_sources / _sourcename(app, docname)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(expanded, encoding="utf-8")


def setup(app):
    app.connect("build-finished", write_expanded_sources)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
