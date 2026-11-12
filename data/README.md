# data

The data files the harnesses read: the prompt sets and the language corpus. They
are here rather than inline in a script so a prompt can be read, quoted and
reproduced without opening a `.py` file.

| File | Read by | What it holds |
| :--- | :--- | :--- |
| [`grammar-prompts.json`](grammar-prompts.json) | `scripts/measure/grammar-test.py` | The format-adherence schemas, each with one good and one bad answer |
| [`redteam-prompts.json`](redteam-prompts.json) | `scripts/security/redteam-benchmark.py` | The four web challenges, the reply instruction, the RE prompt template |
| [`languages.json`](languages.json) | `scripts/measure/hallucination-test.py` | 102 languages, each with a real API and a fabricated twin |

## Shape

- **grammar-prompts.json** carries the schemas and, beside each one, a good and
  a bad answer. `grammar-test.py --selftest` grades those two, so the file that
  defines a task also proves the validator against it.
- **redteam-prompts.json** carries the challenges and both prompt strings. The
  reverse-engineering template holds `{strings}` and `{disasm}` placeholders the
  harness fills at run time from the challenge binary it compiled.
- **languages.json** pairs every language with a genuine API for it and a twin
  that does not exist. The hallucination probe asks a model to call both; the
  scorer measures how often it calls the fake one real.

## Adding an entry

Keep the category declared and the ids unique — the offline gate fails
otherwise. For a language, the twin must differ from the real name, and both must
be plausible; `test/test.sh` step 14 proves the corpus still has that property.
