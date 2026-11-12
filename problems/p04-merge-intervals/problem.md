# P04 — Merge Intervals

## Statement

Given a list of intervals `intervals` (each `[start, end]` with `start <= end`),
merge all overlapping intervals and return the non-overlapping intervals that
cover every input interval, **sorted by start**.

Two intervals overlap if one starts at or before the other ends.

## Examples

```text
[[1,3],[2,6],[8,10],[15,18]]  ->  [[1,6],[8,10],[15,18]]
[[1,4],[4,5]]                 ->  [[1,5]]
[[1,4],[0,4]]                 ->  [[0,4]]
```

## Constraints

- `0 <= len(intervals) <= 10^4`
- `0 <= start <= end <= 10^4`

## Signature

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    ...
```

Cases: [`tests/test-cases.json`](tests/test-cases.json). Reference:
[`solutions/solution.py`](solutions/solution.py).
