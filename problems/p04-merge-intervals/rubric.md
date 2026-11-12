# Rubric — P04 Merge Intervals

Scored by the harness, not by a human.

| Dimension | Weight | How |
| :--- | ---: | :--- |
| Correctness | 100% | the returned list must equal the expected list (intervals in start order) |

A solution that returns merged intervals in the wrong order, or leaves touching
intervals (`[1,4]` and `[4,5]`) unmerged, scores zero on the affected cases.
Empty input must return `[]`.

Reference: [`solutions/solution.py`](solutions/solution.py).
