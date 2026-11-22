# Coding benchmark — does the code pass?

**Date:** 2026-11-22. Each model was asked for a Python solution to 5 problem(s); the code was run against hidden cases and scored.

| Model | p01 | p02 | p03 | p04 | p05 | Total |
|---|:---:|:---:|:---:|:---:|:---:|---:|
| `GLM-4.7-Flash-8bit` (`glm47`) | 12/12 | 2/10 | 5/10 | ❌ | ❌ | **19/32** |
| `GLM-4.7-Flash-8bit` (`glm47-hot`) | 12/12 | 5/10 | ❌ | 3/12 | 1/12 | **21/46** |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear`) | 12/12 | 10/10 | 5/10 | 12/12 | 12/12 | **51/56** |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear-hot`) | 12/12 | 10/10 | 10/10 | 12/12 | 12/12 | **56/56** |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling`) | 12/12 | 10/10 | ❌ | 12/12 | 12/12 | **46/46** |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-hot`) | 12/12 | 10/10 | ❌ | 12/12 | 12/12 | **46/46** |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp`) | 12/12 | 10/10 | ❌ | 12/12 | 12/12 | **46/46** |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp-hot`) | 12/12 | 10/10 | ❌ | 12/12 | 12/12 | **46/46** |

## `GLM-4.7-Flash-8bit` · `glm47`

- **p01-two-sum:** 12/12 in 9.7s
- **p02-longest-increasing-subsequence:** 2/10 in 7.9s; failed: classic, plateaus, all_equal, decreasing, increasing, negatives, with_dupes_inside, long_mixed
- **p03-median-two-sorted:** 5/10 in 16.9s; failed: odd, empty_first, empty_second, all_left, negatives
- **p04-merge-intervals:** function 'merge_intervals' not defined (top-level error: invalid syntax (solution.py, line 22))
- **p05-word-break:** function 'word_break' not defined (top-level error: invalid syntax (solution.py, line 1))

## `GLM-4.7-Flash-8bit` · `glm47-hot`

- **p01-two-sum:** 12/12 in 7.0s
- **p02-longest-increasing-subsequence:** 5/10 in 8.3s; failed: classic, increasing, negatives, with_dupes_inside, long_mixed
- **p03-median-two-sorted:** function 'find_median' not defined (top-level error: invalid syntax (solution.py, line 1))
- **p04-merge-intervals:** 3/12 in 6.8s; failed: classic, touching, nested, no_overlap, unsorted_input, contained, duplicate_starts, chain, gap_at_zero
- **p05-word-break:** 1/12 in 10.3s; failed: classic_true, reuse, prefix_trap, single_word, no_match, seam, whole_word, many_singles, overlap_words, two_piece, impossible_tail

## `Kimi-Linear-48B-A3B-Instruct-4bit` · `kimi-linear`

- **p01-two-sum:** 12/12 in 1.9s
- **p02-longest-increasing-subsequence:** 10/10 in 3.4s
- **p03-median-two-sorted:** 5/10 in 8.1s; failed: odd, empty_first, empty_second, all_left, negatives
- **p04-merge-intervals:** 12/12 in 3.7s
- **p05-word-break:** 12/12 in 2.9s

## `Kimi-Linear-48B-A3B-Instruct-4bit` · `kimi-linear-hot`

- **p01-two-sum:** 12/12 in 1.3s
- **p02-longest-increasing-subsequence:** 10/10 in 1.9s
- **p03-median-two-sorted:** 10/10 in 6.6s
- **p04-merge-intervals:** 12/12 in 2.3s
- **p05-word-break:** 12/12 in 1.9s

## `Inkling-2-Mini-oQ4e-mtp` · `inkling`

- **p01-two-sum:** 12/12 in 9.4s
- **p02-longest-increasing-subsequence:** 10/10 in 15.9s
- **p03-median-two-sorted:** function 'find_median' not defined
- **p04-merge-intervals:** 12/12 in 21.2s
- **p05-word-break:** 12/12 in 21.1s

## `Inkling-2-Mini-oQ4e-mtp` · `inkling-hot`

- **p01-two-sum:** 12/12 in 7.7s
- **p02-longest-increasing-subsequence:** 10/10 in 12.7s
- **p03-median-two-sorted:** function 'find_median' not defined
- **p04-merge-intervals:** 12/12 in 14.9s
- **p05-word-break:** 12/12 in 21.0s

## `Inkling-2-Mini-oQ4e-mtp` · `inkling-mtp`

- **p01-two-sum:** 12/12 in 13.9s
- **p02-longest-increasing-subsequence:** 10/10 in 18.6s
- **p03-median-two-sorted:** function 'find_median' not defined (top-level error: invalid syntax (solution.py, line 1))
- **p04-merge-intervals:** 12/12 in 17.0s
- **p05-word-break:** 12/12 in 18.8s

## `Inkling-2-Mini-oQ4e-mtp` · `inkling-mtp-hot`

- **p01-two-sum:** 12/12 in 9.3s
- **p02-longest-increasing-subsequence:** 10/10 in 13.2s
- **p03-median-two-sorted:** function 'find_median' not defined
- **p04-merge-intervals:** 12/12 in 16.0s
- **p05-word-break:** 12/12 in 22.6s
