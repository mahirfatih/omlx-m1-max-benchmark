# P01 — Two-Sum (O(n))

## Statement

Given a list of integers `nums` and an integer `target`, return the **indices**
`[i, j]` (with `i < j`) of the two numbers that add up to `target`.

Exactly one solution exists, and you may not use the same element twice. Return
the answer in any order.

**Aim for O(n) time.** The cases include arrays large enough that the scoring
prefers the hash-map solution.

## Examples

```text
nums = [2, 7, 11, 15], target = 9   ->  [0, 1]
nums = [3, 2, 4],      target = 6   ->  [1, 2]
nums = [3, 3],         target = 6   ->  [0, 1]
```

## Constraints

- `2 <= len(nums) <= 10000`
- `-10^9 <= nums[i] <= 10^9`
- Exactly one valid answer exists.

## Signature

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    ...
```

## What is scored

All hidden cases must pass. The rubric is in [`rubric.md`](rubric.md); the cases
are in [`tests/test-cases.json`](tests/test-cases.json).
