# `docs/overview/` — what was measured

The benchmark in one page, and the background needed to read the numbers.

- [`README.md`](README.md) — machine, method, headline result.
- [`BACKGROUND.md`](BACKGROUND.md) — what oMLX is, and why the measurements look the way they do.

## The one-paragraph version

Six local LLMs, all 4-bit MLX builds, were served by
[oMLX](https://omlx.ai) 0.7.3 on an **Apple M1 Max with 64 GB** of unified memory
running **macOS 26.7.2**. Each model was unloaded, loaded on demand, warmed up,
then asked the same English and Turkish prompt twice. Throughput was
`completion_tokens / wall_time`. The fastest model was **Qwen3.6-35B-A3B** at
**73.4 tok/s** average; the slowest was **Qwen3.8-27B-Uncensored** at
**18.2 tok/s**. Full numbers are in
[`../reference/RESULTS.md`](../reference/RESULTS.md).

## Why this exists

Two questions motivate the repository:

1. **How fast is a single Apple M1 Max actually, on a 35B-class MoE model, with a
   tuned server?** The headline answer — around 60–73 tok/s for the fast
   MoE models — is what makes local agentic coding practical on this hardware.
2. **Which of the locally installed models are uncensored, and by which method?**
   Several are abliterated ("heretic") builds. The repository documents that
   classification with source evidence, in
   [`../reference/MODELS.md`](../reference/MODELS.md).

## What this is not

- It is **not** a model-quality leaderboard. Throughput says nothing about
  reasoning, coding or instruction-following quality.
- It is **not** a comparison against cloud APIs or other hardware. Every number
  is one machine, one server version, one prompt pair.
- It is **not** a tuning guide for other Apple chips. An M1 Max has ~400 GB/s of
  memory bandwidth; an M3 Ultra has several times that, so the relative ranking
  may hold while the absolute numbers do not.
