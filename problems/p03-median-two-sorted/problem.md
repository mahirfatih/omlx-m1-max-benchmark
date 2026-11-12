# P03 — Median of Two Sorted Arrays

## Statement

Given two sorted arrays `nums1` and `nums2`, return the **median** of the
combined array as a float.

You may assume at least one of the arrays is non-empty. An `O(log(m+n))` solution
is the target; a merge is accepted for correctness but is the reason this problem
is marked *expert*.

## Examples

```text
nums1 = [1, 3], nums2 = [2]         ->  2.0
nums1 = [1, 2], nums2 = [3, 4]      ->  2.5
nums1 = [],     nums2 = [1]         ->  1.0
```

## Constraints

- `0 <= len(nums1), len(nums2) <= 1000`
- `1 <= len(nums1) + len(nums2) <= 2000`
- Both arrays are sorted ascending.

## Signature

```python
def find_median(nums1: list[int], nums2: list[int]) -> float:
    ...
```

Cases: [`tests/test-cases.json`](tests/test-cases.json). Reference:
[`solutions/solution.py`](solutions/solution.py).
