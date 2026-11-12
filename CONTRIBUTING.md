# Contributing

Thanks for your interest! This repository is primarily a benchmark snapshot, but corrections and additional data points are welcome.

## Reporting a measurement

If you run the benchmark on different hardware, please include:

- Chip, RAM, macOS version
- oMLX version
- Quantization and context settings
- The raw output of `python3 scripts/measure/benchmark.py`

Open an issue or a pull request with the generated Markdown report under `benchmarks/`.

## Pull requests

1. Fork the repository and create a topic branch.
2. Keep changes focused and reproducible.
3. Update `README.md` if you add or change results.
4. Do **not** commit API keys, tokens or other secrets.

## Code style

- Python scripts should stay dependency-free (standard library only).
- Use clear, commented code and keep output human-readable.
