---
name: create-revealjs-slide
description: Create, draft, edit, and polish Reveal.js slide decks written in reStructuredText in this repository. Use when Codex needs to turn source material such as blog posts, notes, demos, or talk outlines into sphinx-revealjs slides; adjust slide structure for LT talks; build the generated HTML; inspect slides with Chrome DevTools MCP; and fix overflowing text, cramped diagrams, tables, or code blocks.
---

# Create Reveal.js Slide

Create or polish reST slide decks that build to Reveal.js with Sphinx. Prefer a complete workflow: understand the talk, draft or edit the reST, build, inspect the generated HTML, adjust layout, and clean up temporary artifacts.

## Workflow

1. Read the source material and nearby slide files to learn the repo's style.
2. Clarify the talk shape from context: event, duration, demo order, audience, and what listeners should be able to reproduce.
3. Draft or edit the target `.rst` using existing project conventions.
4. Build with `make slide`.
5. Open the generated HTML through a local HTTP server and inspect it with Chrome DevTools MCP.
6. Fix slide-level issues: overflowing text, cramped diagrams, tiny Mermaid labels, wide tables, long URLs, and hard-to-read code blocks.
7. Rebuild and re-check until the important slides are readable.
8. Stop the HTTP server and delete temporary screenshots.

## Drafting Slides

Use the talk's actual flow, not the source article's order. For LT talks, slides often work better as a short map for the audience than as a complete transcript.

When a demo happens before slides, structure the deck as "what you just saw" followed by "how to reproduce it." Prioritize:

- the minimal architecture or mental model
- concrete setup steps
- configuration values that matter
- quick checks for failure cases
- a short summary

Keep slides sparse. Move details to speaker notes, references, or the source article when the audience does not need them on screen.

## reST Conventions

Follow nearby files in `source/**.rst` for section levels, metadata, code blocks, footnotes, and raw HTML. Common patterns:

```rst
:ogp_title: <title>
:ogp_event_name: <event>
:ogp_slide_name: <slide>
:ogp_description: <short description>

======================================================================
<Title>
======================================================================

:Event: <event name>
:Presented: <date> <speaker>
```

Use `.. code-block:: console` for terminal commands. Keep code blocks short enough to read at presentation size.

### Heading Hierarchy

Use H3-level headings as well as H2 when a topic has concrete examples, steps, or follow-up slides. Do not flatten every slide into H2. Follow this repository's adornment order:

- H1: deck title, `=` overline and underline.
- H2: main topic, `=` underline.
- H3: details within that topic, `-` underline.

```rst
==============================
Deck title
==============================

Main topic
==============================

Overview of this topic.

Concrete example
------------------------------

Details on their own slide.

Next main topic
==============================
```

reST determines heading levels by adornment order, not by the character alone. In sphinx-revealjs, H3 sections become vertical slides within the H2 topic. Verify both horizontal and vertical navigation; do not treat H3 as an inline label on the same slide.

### Speaker Notes

Write speaker notes as reST **comments**, not raw HTML `<aside>` blocks. Put timing and spoken explanation in one comment block per slide:

```rst
Concrete example
------------------------------

* Visible slide content

.. 【30秒／累計2:00】
   Explain this example verbally.
   Keep additional spoken detail in this same comment block.
```

Check `source/conf.py`: comments are rendered as speaker notes only when `revealjs_notes_from_comments = True` (the default is `False`). Enable it when comments should appear in Speaker View. With this setting, ordinary reST comments also become notes; keep editing reminders out of speaker-note blocks when they are not meant to be spoken. Reveal.js uses only the first notes block per slide, so consolidate notes instead of mixing comments with `revealjs-notes` or raw HTML notes.

See the official [comment-to-notes configuration](https://sphinx-revealjs.readthedocs.io/en/stable/configurations/#confval-revealjs_notes_from_comments) and [Speaker Views migration guide](https://sphinx-revealjs.readthedocs.io/en/stable/upgrade/2.x/#speaker-views). The docs also offer a `revealjs-notes` directive; this repository prefers comments.

## Build

Run:

```bash
make slide
```

If Sphinx fails with `unsupported locale setting`, retry:

```bash
env LC_ALL=C LANG=C make slide
```

If `uv` cache access fails under the sandbox, rerun the same build command with escalation. Treat `document isn't included in any toctree` warnings as expected when existing decks show the same warning pattern.

## Chrome Inspection

Serve generated slides over HTTP; direct `file://` navigation can be unreliable.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory build/revealjs
```

Open:

```text
http://127.0.0.1:8765/<event>/<slide>.html
```

Use Chrome DevTools MCP to resize to a presentation-like viewport, commonly `1440x900`, then verify navigation with `ArrowRight` and `ArrowDown` for H3 slides (or `Space` to traverse the whole deck).

## Overflow Check

Use Chrome DevTools MCP `evaluate_script` to scan all slides for elements outside the slide bounds:

```js
async () => {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const results = [];
  const slides = Reveal.getSlides();

  for (let i = 0; i < slides.length; i++) {
    const indices = Reveal.getIndices(slides[i]);
    Reveal.slide(indices.h, indices.v || 0, 0);
    await sleep(150);

    const slide = Reveal.getCurrentSlide();
    const slideRect = slide.getBoundingClientRect();
    const bad = [...slide.querySelectorAll("h1,h2,h3,p,li,pre,svg,.mermaid,table,dl")]
      .map((el) => {
        if (el.closest("svg, .notes")) return null;
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          text: (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim().slice(0, 70),
          overflowX: rect.left < slideRect.left - 2 || rect.right > slideRect.right + 2,
          overflowY: rect.top < slideRect.top - 2 || rect.bottom > slideRect.bottom + 2,
        };
      })
      .filter(Boolean)
      .filter((item) => item.overflowX || item.overflowY);

    const svg = slide.querySelector("svg");
    results.push({
      index: i + 1,
      h: indices.h,
      v: indices.v || 0,
      title: slide.querySelector("h1,h2,h3")?.innerText?.trim() || "",
      bad,
      svg: svg
        ? {
            w: Math.round(svg.getBoundingClientRect().width),
            h: Math.round(svg.getBoundingClientRect().height),
            viewBox: svg.getAttribute("viewBox"),
            maxWidth: svg.style.maxWidth,
          }
        : null,
      textLen: [...slide.children]
        .filter((el) => !el.matches(".notes"))
        .map((el) => el.innerText || "")
        .join(" ").replace(/\s+/g, " ").trim().length,
    });
  }

  Reveal.slide(0, 0, 0);
  return results;
}
```

Interpretation:

- `bad: []` means no clear DOM-level overflow.
- `overflowY` usually means too much text; shorten or split the slide.
- `overflowX` often points to long URLs, code, or tables.
- A suspicious Mermaid `viewBox` or blank-looking SVG usually means the Mermaid markup or init settings need adjustment.

## Visual Polish

Always inspect screenshots for slides flagged by the DOM scan and any slide that feels visually dense.

Use these fixes first:

- Replace wide tables with concise bullets unless the table is essential.
- Shorten long URLs and commands; explain details verbally or in references.
- Keep code blocks to the shortest runnable form.
- Use Mermaid `flowchart TD` for architecture diagrams when horizontal layout makes labels tiny.
- Avoid aggressive Mermaid `init` styling when it breaks SVG sizing.
- Reduce diagram detail to what the talk explains.
- Split a slide instead of shrinking text when the idea has multiple steps.

## Cleanup

Stop the HTTP server with `Ctrl-C` in the session that started it. Delete temporary screenshots:

```bash
rm /private/tmp/<slide>-*.png
```

Do not delete generated `build/revealjs` files unless the user asks; they are useful for immediate review.
