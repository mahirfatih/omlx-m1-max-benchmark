# Coding benchmark — does the code pass?

**Date:** 2026-11-12. Each model was asked for a Python solution to 5 problem(s); the code was run against hidden cases and scored.

| Model | p01 | p02 | p03 | p04 | p05 | Total |
|---|:---:|:---:|:---:|:---:|:---:|---:|
| `Qwen3.6-35B-A3B-4bit` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Ornith-1.5-35B-A3B-MLX-4bit` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `gemma-4-26B-A4B-it-heretic-4bit` | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Qwen3-Coder-30B-A3B-Instruct-4bit` | 12/12 | 10/10 | ❌ | 12/12 | 11/12 | **45/46** |
| `Qwen3.8-27B-Uncensored-MLX` | 12/12 | 10/10 | ❌ | 12/12 | ❌ | **34/34** |

## `Qwen3.6-35B-A3B-4bit`

- **p01-two-sum:** 12/12 in 1.8s
- **p02-longest-increasing-subsequence:** 10/10 in 1.9s
- **p03-median-two-sorted:** 10/10 in 5.7s
- **p04-merge-intervals:** 12/12 in 2.7s
- **p05-word-break:** 12/12 in 2.2s

## `Qwen3.6-35B-A3B-Uncensored-Heretic-MLX-4bit`

- **p01-two-sum:** 12/12 in 1.6s
- **p02-longest-increasing-subsequence:** 10/10 in 2.1s
- **p03-median-two-sorted:** 10/10 in 6.4s
- **p04-merge-intervals:** 12/12 in 2.9s
- **p05-word-break:** 12/12 in 2.4s

## `Ornith-1.5-35B-A3B-MLX-4bit`

- **p01-two-sum:** 12/12 in 1.9s
- **p02-longest-increasing-subsequence:** 10/10 in 1.9s
- **p03-median-two-sorted:** 10/10 in 5.3s
- **p04-merge-intervals:** 12/12 in 2.7s
- **p05-word-break:** 12/12 in 2.6s

## `gemma-4-26B-A4B-it-heretic-4bit`

- **p01-two-sum:** 12/12 in 2.1s
- **p02-longest-increasing-subsequence:** 10/10 in 3.5s
- **p03-median-two-sorted:** 10/10 in 7.2s
- **p04-merge-intervals:** 12/12 in 3.7s
- **p05-word-break:** 12/12 in 3.0s

## `Qwen3-Coder-30B-A3B-Instruct-4bit`

- **p01-two-sum:** 12/12 in 2.0s
- **p02-longest-increasing-subsequence:** 10/10 in 2.1s
- **p03-median-two-sorted:** function 'find_median' not defined (top-level error: expected an indented block after 'else' statement on line 35 (solution.py, line 37))
- **p04-merge-intervals:** 12/12 in 3.8s
- **p05-word-break:** 11/12 in 3.0s; failed: empty_string

## `Qwen3.8-27B-Uncensored-MLX`

- **p01-two-sum:** 12/12 in 18.4s
- **p02-longest-increasing-subsequence:** 10/10 in 28.5s
- **p03-median-two-sorted:** function 'find_median' not defined
- **p04-merge-intervals:** 12/12 in 30.8s
- **p05-word-break:** function 'word_break' not defined
