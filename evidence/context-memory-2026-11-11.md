# Long-context memory

**Date:** 2026-11-12. Context ~6336 tokens (25344 chars) with facts planted at increasing depth.

| Model | retrieval | conflict | aggregate | Recalled |
|---|:---:|:---:|:---:|---:|
| `Qwen3.6-35B-A3B-4bit` | ✅ | ✅ | ❌ | **2/3** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | ✅ | ✅ | ❌ | **2/3** |
| `Ornith-1.5-35B-A3B-MLX-4bit` | ✅ | ✅ | ❌ | **2/3** |
| `gemma-4-26B-A4B-it-heretic-4bit` | ✅ | ✅ | ❌ | **2/3** |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | ✅ | ✅ | ❌ | **2/3** |
| `Qwen3.8-27B-Uncensored-MLX` | ❌ | ❌ | ❌ | **0/3** |
