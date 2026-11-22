# Hallucination & error risk

**Date:** 2026-11-22. 102 languages × 2 probes (one genuine API/feature, one fabricated twin).

| Model | Answered | Accuracy | Hallucination (fake → “real”) | False alarm (real → “fake”) | Brier ↓ | Overconfident + wrong |
|---|---:|---:|---:|---:|---:|---:|
| `GLM-4.7-Flash-8bit` (`glm47`) | 165/204 | 98% (161/165) | **2%** (2/85) | 2% (2/80) | 0.11 | 3 |
| `GLM-4.7-Flash-8bit` (`glm47-hot`) | 165/204 | 98% (161/165) | **2%** (2/85) | 2% (2/80) | 0.11 | 3 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling`) | 188/204 | 100% (188/188) | **0%** (0/94) | 0% (0/94) | 0.004 | 0 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-hot`) | 188/204 | 100% (188/188) | **0%** (0/94) | 0% (0/94) | 0.004 | 0 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp`) | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.005 | 0 |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp-hot`) | 204/204 | 100% (204/204) | **0%** (0/102) | 0% (0/102) | 0.007 | 0 |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear`) | 204/204 | 100% (203/204) | **0%** (0/102) | 1% (1/102) | 0.005 | 1 |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear-hot`) | 204/204 | 100% (203/204) | **0%** (0/102) | 1% (1/102) | 0.005 | 1 |

_Hallucination = a fabricated API or feature the model called real. False alarm = a genuine one it called fake. Brier = mean squared error of the stated confidence; 0 is perfect, 0.25 is a coin flip, lower is better, and it is computed only over answers that stated a confidence._

## Most-fooled languages (pooled over models)

| Language | Models that called the fake real |
|---|---:|
| `matlab` | 2/8 |
| `objective-c` | 2/8 |
