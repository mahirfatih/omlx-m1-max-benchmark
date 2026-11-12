# Architecture — the request path

Written companion to
[`architecture.html`](architecture.html). The HTML is the interactive version;
this page is the one GitHub renders and a reviewer diffs.

## One request, end to end

```mermaid
flowchart TD
    C["Client<br/>OpenCode · script · curl"]
    A["oMLX API<br/>uvicorn · 127.0.0.1:8000 · auth"]
    G["Memory guard<br/>prefill estimate · aggressive"]
    S["Scheduler<br/>continuous batching · 1 request"]
    R["MLX runtime<br/>4-bit weights · 4-bit KV cache"]
    D["SSD KV cache<br/>turboquant blocks · LRU"]

    C -->|"POST /v1/chat/completions"| A
    A -->|"load estimate"| G
    G -->|"accept / reject"| S
    S -->|"batched prompt"| R
    R -->|"restore prefix"| D
    R -->|"stream tokens"| C
```

## The sequence

```mermaid
sequenceDiagram
    participant Client
    participant API as oMLX API
    participant Guard as Memory guard
    participant Sched as Scheduler
    participant RT as MLX runtime
    participant Disk as SSD KV cache

    Client->>API: POST /v1/chat/completions (Bearer key)
    API->>API: authenticate
    API->>Guard: estimate prefill memory
    alt fits
        Guard->>Sched: accept
        Sched->>RT: batched prompt
        RT->>Disk: restore matching prefix blocks
        Disk-->>RT: cached KV (if any)
        RT-->>Client: stream tokens
    else too large
        Guard-->>Client: 4xx — load rejected, no OOM
    end
```

## The profile decision

Which settings a request runs with is decided by the model → profile mapping, not
by the client:

```mermaid
flowchart LR
    M["Model id"] --> MAP{"model → profile"}
    MAP -->|"Qwen3 · Ornith · Coder"| Q["qwen3<br/>max_tokens 4096"]
    MAP -->|"Heretic · Qwen3.8"| H["qwen36-heretic<br/>max_tokens 2048"]
    MAP -->|"gemma-4"| G["gemma4-heretic<br/>max_tokens 2048"]
    Q --> S["shared sampling<br/>temp 0.2 · top_p 0.95 · 4-bit KV"]
    H --> S
    G --> S
```

## The benchmark pipeline

How a number gets into the README:

```mermaid
flowchart LR
    B["scripts/measure/benchmark.py"] --> R["benchmarks/&lt;date&gt;.md"]
    R --> J["reference/results.json"]
    J --> A["scripts/analysis/analyze-results.py"]
    A --> MD["README charts + docs/reference/RESULTS.md"]
    J --> MF["scripts/release/build-manifest.py"]
    MF --> MAN["manifest.json"]
    MAN --> CHK["test/test.sh"]
```

## Notes

- **Loopback only.** The API binds `127.0.0.1`; there is no remote listener. See
  [`../security/README.md`](../../security/README.md).
- **One model at a time.** `max_concurrent_requests` is 1; the scheduler's
  batching exists but is not exercised by this benchmark.
- **The guard is the safety valve.** A third large model is rejected by the
  prefill estimate rather than crashing the machine.
