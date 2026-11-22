# Code-syntax matrix — 2026-11-22 campaign

**Date:** 2026-11-22. Each model (profile) was asked for one small function per
language — a `top3(lst)` in Python, a `reverseStr(s)` in JavaScript, a
`.log`-counting Bash script and an `evens(_:)` in Swift — and the returned code
was handed to that language's own checker (`python -m py_compile`, `node --check`,
`bash -n`, `swiftc -parse`). A model that returns no code at all is recorded as
`empty`, not as a syntax failure.

| Model (profile) | python | nodejs | bash | swift |
| :--- | :---: | :---: | :---: | :---: |
| `GLM-4.7-Flash-8bit` (`glm47`) | ✅ | ✅ | ✅ | ✅ |
| `GLM-4.7-Flash-8bit` (`glm47-hot`) | ✅ | ✅ | ✅ | ✅ |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear`) | ✅ | ✅ | ✅ | ✅ |
| `Kimi-Linear-48B-A3B-Instruct-4bit` (`kimi-linear-hot`) | ✅ | ✅ | ✅ | ✅ |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling`) | ❌ empty | ✅ | ❌ empty | ✅ |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-hot`) | ❌ empty | ✅ | ❌ empty | ✅ |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp`) | ❌ empty | ✅ | ❌ empty | ✅ |
| `Inkling-2-Mini-oQ4e-mtp` (`inkling-mtp-hot`) | ❌ empty | ✅ | ❌ empty | ✅ |

GLM and Kimi returned syntactically valid code in all four languages. **Inkling
returned no code at all for the Python and Bash prompts, in all four profiles** —
the same thinking-block behaviour that empties its short answers elsewhere, not a
syntax error in code it wrote. Its Node and Swift answers were valid.

Raw transcript (`scripts/measure/code-matrix-test.py`, `--models` for the eight
profiles):

```text
MODEL: GLM-4.7-Flash-8bit | profil: glm47
  [python] OK   | python compile OK |  11.8s
  [nodejs] OK   | node --check OK |   2.4s
  [bash  ] OK   | bash -n OK |   2.3s
  [swift ] OK   | swiftc -parse OK |   1.9s
MODEL: GLM-4.7-Flash-8bit | profil: glm47-hot
  [python] OK   | python compile OK |  11.6s
  [nodejs] OK   | node --check OK |   2.5s
  [bash  ] OK   | bash -n OK |   2.4s
  [swift ] OK   | swiftc -parse OK |   1.3s
MODEL: Kimi-Linear-48B-A3B-Instruct-4bit | profil: kimi-linear
  [python] OK   | python compile OK |   7.6s
  [nodejs] OK   | node --check OK |   0.7s
  [bash  ] OK   | bash -n OK |   1.1s
  [swift ] OK   | swiftc -parse OK |   1.0s
MODEL: Kimi-Linear-48B-A3B-Instruct-4bit | profil: kimi-linear-hot
  [python] OK   | python compile OK |   7.1s
  [nodejs] OK   | node --check OK |   0.5s
  [bash  ] OK   | bash -n OK |   1.0s
  [swift ] OK   | swiftc -parse OK |   0.8s
MODEL: Inkling-2-Mini-oQ4e-mtp | profil: inkling
  [python] FAIL | bos cikti |  20.5s
  [nodejs] OK   | node --check OK |  15.9s
  [bash  ] FAIL | bos cikti |  15.9s
  [swift ] OK   | swiftc -parse OK |  15.6s
MODEL: Inkling-2-Mini-oQ4e-mtp | profil: inkling-hot
  [python] FAIL | bos cikti |  19.2s
  [nodejs] OK   | node --check OK |  15.4s
  [bash  ] FAIL | bos cikti |  15.5s
  [swift ] OK   | swiftc -parse OK |  15.0s
MODEL: Inkling-2-Mini-oQ4e-mtp | profil: inkling-mtp
  [python] FAIL | bos cikti |  19.0s
  [nodejs] OK   | node --check OK |  15.4s
  [bash  ] FAIL | bos cikti |  15.3s
  [swift ] OK   | swiftc -parse OK |  14.8s
MODEL: Inkling-2-Mini-oQ4e-mtp | profil: inkling-mtp-hot
  [python] FAIL | bos cikti |  18.1s
  [nodejs] OK   | node --check OK |  14.9s
  [bash  ] FAIL | bos cikti |  15.1s
  [swift ] OK   | swiftc -parse OK |  14.6s
```
