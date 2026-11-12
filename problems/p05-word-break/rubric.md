# Rubric — P05 Word Break

Scored by the harness, not by a human.

| Dimension | Weight | How |
| :--- | ---: | :--- |
| Correctness | 100% | the returned boolean must match for every case |

The cases include the two classic traps: a word that is a prefix but leaves an
unbreakable tail (`catsandog`), and reuse of the same word (`applepenapple`).
The empty string is `False`.

Reference: [`solutions/solution.py`](solutions/solution.py).
