# Rubric — P01 Two-Sum

Scored by the harness, not by a human.

| Dimension | Weight | How |
| :--- | ---: | :--- |
| Correctness | 100% | fraction of hidden cases that return the right indices |

A solution that returns the *values* instead of the *indices* scores zero: the
runner compares index lists (order-insensitive). A brute-force O(n²) solution is
correct on these cases and scores full marks — this problem measures
correctness, not speed; the throughput benchmark measures speed.

Reference: [`solutions/solution.py`](solutions/solution.py).
