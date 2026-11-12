# `docs/diagrams/` — the diagram output

The interactive diagram and its written companion. Both describe the same thing:
one request's path through oMLX on this machine.

- [`architecture/architecture.html`](architecture/architecture.html) — the
  click-through diagram (self-contained, open it in a browser).
- [`architecture/architecture.md`](architecture/architecture.md) — the written
  companion, with Mermaid versions of the same flow.
- [`../architecture/source.json`](../architecture/source.json) — the outline the
  HTML is built from.

## Editing

Change [`../architecture/source.json`](../architecture/source.json) and update the
`DATA` object in the HTML to match, then open the HTML. There is no build step;
the file is self-contained (inline CSS and JS, no external requests), so it works
offline and from a `file://` URL.

Hand-editing only the HTML is fine for a visual tweak, but the JSON is the source
of truth for the nodes and edges — keep the two in agreement.

## Why an HTML diagram plus a Markdown one

GitHub renders the Markdown and its Mermaid blocks in the repository view; the
HTML gives the full click-through experience when opened locally. The Markdown is
the one that survives a `git clone` and a code review.
