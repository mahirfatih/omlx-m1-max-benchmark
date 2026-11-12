# P05 — Word Break

## Statement

Given a string `s` and a list of dictionary words `word_dict`, return `True` if
`s` can be segmented into a space-separated sequence of one or more dictionary
words, and `False` otherwise.

Words may be reused any number of times.

## Examples

```text
s = "leetcode",     word_dict = ["leet","code"]          -> True
s = "applepenapple", word_dict = ["apple","pen"]        -> True
s = "catsandog",    word_dict = ["cats","dog","sand","and","cat"] -> False
```

## Constraints

- `0 <= len(s) <= 300`
- `1 <= len(word_dict) <= 1000`
- All words and `s` are lowercase letters (the empty string is `False`).

## Signature

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    ...
```

Cases: [`tests/test-cases.json`](tests/test-cases.json). Reference:
[`solutions/solution.py`](solutions/solution.py).
