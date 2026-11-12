# Background — what oMLX is

**[oMLX](https://omlx.ai)** is a macOS-native local LLM server built on
[Apple MLX](https://github.com/ml-explore/mlx). It exposes an
**OpenAI-compatible** API (`/v1/chat/completions`) plus a native
**Anthropic-compatible** endpoint (`/v1/messages`), so any client that speaks
either protocol can use it as a drop-in backend.

- Website: <https://omlx.ai>
- Source: <https://github.com/jundot/omlx>
- Licence: Apache 2.0 · Apple Silicon · macOS 15+
- This benchmark used **oMLX 0.7.3**.

## Why oMLX, and not Ollama or LM Studio

The difference that matters for agents is **KV-cache persistence**. Ollama and
LM Studio keep the KV cache in memory; when the context shifts mid-session — which
happens constantly with coding agents — the cache is invalidated and recomputed
from scratch. oMLX persists every KV-cache block to **SSD in safetensors format**
with a two-tier (RAM + SSD, LRU) policy, so a previously seen prefix is restored
across requests and server restarts instead of recomputed.

The practical effect oMLX advertises is **time-to-first-token dropping from
30–90 s to under 5 s** on long contexts from the second turn. That is a
latency claim, not a throughput claim; this repository measures **decode
throughput**, which is a different axis (see
[`../guides/METHODOLOGY.md`](../guides/METHODOLOGY.md)).

oMLX also provides continuous batching (`mlx-lm` `BatchGenerator`), multi-model
serving with LRU eviction, tool-calling and MCP support, and a menu-bar app with
a web dashboard.

## Why the numbers look the way they do

Three properties of the setup shape the results:

- **4-bit weights.** Every model is an MLX 4-bit quantization. On a
  memory-bandwidth-bound machine, a smaller weight footprint decodes faster.
  This is the single biggest reason the 35B MoE models beat the 27B *dense*
  model: the MoE activates only ~3B parameters per token, while the dense model
  reads all 27B weights per token.
- **Mixture-of-Experts.** Five of the six models are MoE: the total parameter
  count is large but the **active** count per token is small (~3–4B). Throughput
  tracks the active count and the bandwidth, not the total count.
- **Stable sampling.** All runs use `temperature 0.2`, `top_p 0.95`,
  `top_k 20`, `repetition_penalty 1.1`, `min_p 0.05`, `presence_penalty 0.3`,
  thinking **off**, and a **4-bit KV cache**. These are the same settings the
  profiles ship with; see [`../reference/PROFILES.md`](../reference/PROFILES.md).

## Hardware context

The M1 Max (2021) has up to **64 GB** of unified memory and roughly
**400 GB/s** of memory bandwidth. Decode speed for a memory-bound model is
approximately `bandwidth / bytes-read-per-token`; a 4-bit, ~18 GB model that
reads only the active experts lands in the tens of tokens per second, which is
what the table shows. Newer Max/Ultra parts have proportionally more bandwidth,
so their absolute numbers would be higher while the relative order of these
models is unlikely to change.
