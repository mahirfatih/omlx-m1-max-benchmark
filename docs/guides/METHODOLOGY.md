# Methodology

What was measured, how, and what a number in the table actually means.

## The metric

**Decode throughput**, in tokens per second:

```text
tok/s = completion_tokens / wall_time_seconds
```

`completion_tokens` is read from the server's `usage` field; if the server omits
it, the script falls back to `len(text) // 4`. `wall_time` is measured by the
client around the HTTP request, so it includes network and queueing on the
loopback socket — negligible here, since the server is on the same machine.

This is a **generation** metric. It is *not* time-to-first-token (prompt
processing) and *not* total request latency. A model can be fast at decoding and
slow to start; oMLX's headline claim is about TTFT, which this repository does
not measure.

## The procedure, per model

1. **Unload everything.** Every known model is sent to `/v1/models/<id>/unload`,
   so the measurement does not compete for memory with a previously loaded model.
2. **Warm-up.** A one-token request loads the model into RAM and pays the cold
   load. Its wall time is recorded separately as **load (s)**.
3. **Measure.** The same prompt is sent in **English** and **Turkish**, **twice
   each**. Each response is capped at `max_tokens 220`.
4. **Average.** EN and TR averages are computed over their two reps; the model
   average is over all four.

The prompts are fixed and identical across models:

- **EN** — "Write a short technical explanation of about 120 words on how a hash
  table works, then give one small example."
- **TR** — the same request in Turkish.

Using one prompt pair keeps the comparison controlled. It also means the numbers
reflect *this* output length and *this* content; a different prompt length would
move the tokens-per-second figure somewhat, because fixed per-request overheads
amortise differently.

## Settings held constant

| Setting | Value |
| :--- | :--- |
| Context window | 32768 |
| Max tokens | 220 (benchmark cap) |
| Temperature | 0.2 |
| Top-p / Top-k | 0.95 / 20 |
| Repetition penalty | 1.1 |
| Min-p | 0.05 |
| Presence penalty | 0.3 |
| Thinking | off |
| KV cache | 4-bit (turboquant) |
| Model residency | lazy, one at a time, 180 s idle unload |

These match the shipped profiles except for `max_tokens`, which the benchmark
overrides to 220 so that every model stops at the same length.

## What varies and what does not

- **Varies:** model architecture (MoE vs dense), active parameter count, weight
  quantization details, tokenizer.
- **Does not vary:** machine, OS, oMLX version, sampling settings, prompt,
  output cap, concurrency (always one request at a time).

## Sources of noise

- **Background load.** Any other process using the GPU or memory shifts the
  numbers. The two reps and the EN/TR split are there partly to expose a noisy
  run — a large EN-vs-TR gap on a model that should be symmetric usually means
  interference, not a real difference.
- **Thermal state.** A long session throttles an M1 Max. Runs are kept short
  (one prompt pair per model) to stay within the boost window.
- **Cold vs warm.** Load time is measured once, on the first (cold) request. It
  is not a steady-state number.

## How to read the ranking

The ranking orders models by **decode speed only**. It is not a quality
ranking. Qwen3.8-27B-Uncensored is last on speed and would be a poor choice for a
latency-sensitive loop; it may still be the right model for tasks where its size
or its uncensored behaviour matters more than speed. See
[`CHOOSING-A-MODEL.md`](CHOOSING-A-MODEL.md).
