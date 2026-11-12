"""Reference solution — Median of Two Sorted Arrays, O(m+n) merge.

A binary-search O(log(min(m,n))) solution is also valid; this one keeps the
reference short and obviously correct. Correctness is what is scored.
"""


def find_median(nums1: list[int], nums2: list[int]) -> float:
    merged = sorted(nums1 + nums2)
    n = len(merged)
    if n == 0:
        return 0.0
    mid = n // 2
    if n % 2 == 1:
        return float(merged[mid])
    return (merged[mid - 1] + merged[mid]) / 2.0


if __name__ == "__main__":
    assert find_median([1, 3], [2]) == 2.0
    assert find_median([1, 2], [3, 4]) == 2.5
    assert find_median([], [1]) == 1.0
    print("ok")
