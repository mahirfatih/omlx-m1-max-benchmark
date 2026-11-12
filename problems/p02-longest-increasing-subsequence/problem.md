# P02 — Longest Increasing Subsequence

## Statement

Given a list of integers `nums`, return the length of the longest strictly
increasing subsequence.

A subsequence keeps the original order but need not be contiguous.

## Examples

```text
nums = [10, 9, 2, 5, 3, 7, 101, 18]   ->  4      # [2, 3, 7, 101]
nums = [0, 1, 0, 3, 2, 3]             ->  4
nums = [7, 7, 7, 7]                    ->  1
```

## Constraints

- `0 <= len(nums) <= 2500`
- `-10^4 <= nums[i] <= 10^4`

## Signature

```python
def length_of_lis(nums: list[int]) -> int:
    ...
```

Cases: [`tests/test-cases.json`](tests/test-cases.json). Reference:
[`solutions/solution.py`](solutions/solution.py).
