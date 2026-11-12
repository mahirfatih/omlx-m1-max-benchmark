# `docs/architecture/` — the diagram's input

The outline the interactive diagram in [`../diagrams/architecture/`](../diagrams/architecture/)
is built from, plus the written explanation of what it shows.

- [`README.md`](README.md) — this file.
- [`source.json`](source.json) — the nodes and edges (the diagram's source of truth).

## What the diagram shows

A single request's path through the stack:

1. **Client** — an OpenAI-compatible client (OpenCode, a script, `curl`).
2. **oMLX API** — the FastAPI/uvicorn server on `127.0.0.1:8000`, which
   authenticates, routes, and enforces the memory guard.
3. **Scheduler** — continuous batching, one request at a time in this
   configuration.
4. **Model runtime** — the MLX engine holding the 4-bit weights and the 4-bit
   KV cache; lazy-loaded, evicted after 180 s idle.
5. **Memory guard** — the prefill estimate that accepts or rejects a model load
   before the OS runs out of memory.

The other diagram in the repository — the profile decision flow, the benchmark
pipeline — lives in the same folder as a Mermaid diagram in
[`../diagrams/architecture/architecture.md`](../diagrams/architecture/architecture.md).

## Regenerating

The HTML is generated from `source.json` by a small inline script. Editing the
JSON and rebuilding is the only supported way to change the diagram; hand-editing
the HTML is lost on the next build. See
[`../diagrams/README.md`](../diagrams/README.md).
