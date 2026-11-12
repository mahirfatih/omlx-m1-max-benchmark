# Hallucination & error risk

**Date:** 2026-11-12. 102 languages × 2 probes (one genuine API/feature, one fabricated twin).

| Model | Answered | Accuracy | Hallucination (fake → “real”) | False alarm (real → “fake”) | Brier ↓ | Overconfident + wrong |
|---|---:|---:|---:|---:|---:|---:|
| `Qwen3.6-35B-A3B-4bit` | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.001 | 0 |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.001 | 0 |
| `gemma-4-26B-A4B-it-heretic-4bit` | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.0 | 0 |
| `Ornith-1.5-35B-A3B-MLX-4bit` | 204/204 | 99% (202/204) | **0%** (0/102) | 2% (2/102) | 0.009 | 1 |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | 182/204 | 99% (180/182) | **0%** (0/91) | 2% (2/91) | 0.006 | 0 |

_Hallucination = a fabricated API or feature the model called real. False alarm = a genuine one it called fake. Brier = mean squared error of the stated confidence; 0 is perfect, 0.25 is a coin flip, lower is better, and it is computed only over answers that stated a confidence._
