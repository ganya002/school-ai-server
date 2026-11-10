# Benchmark Methodology

> Completed in M13-001. Only measured values are recorded; nothing is estimated or copied from the internet.

## Metrics

| Metric | Meaning | How |
| --- | --- | --- |
| Generation (decode) tokens/s | Output speed after the first token | `bench_openai.py` (`decode_tok_s`) or engine timings (Ollama: `eval_count / eval_duration`) |
| Prompt (prefill) tokens/s | How fast the prompt is processed | Engine timings (Ollama: `prompt_eval_count / prompt_eval_duration`; llama.cpp: `timings` in the response) |
| Time to first token (TTFT) | Delay before text appears | `bench_openai.py` (`ttft_s`), streaming |
| Aggregate tokens/s | Total output speed under concurrency | `bench_openai.py --concurrency N` (`round_total_tok_s`) |
| Peak VRAM / power | GPU load | `nvidia-smi --query-gpu=memory.used,power.draw,utilization.gpu --format=csv -l 1` |

## Rules

1. Record the full configuration (GPU, driver, engine version, model file/tag, context, parallel slots) for every run.
2. Warm the model first (`--warmup 1`) unless measuring a cold start, and label it.
3. Use the fixed prompts in [`prompts/`](prompts/): `short.txt`, `medium.txt`, `long.txt`.
4. Use `temperature 0` and a fixed `--max-tokens` (default 256).
5. At least 5 runs per test; report the median and the range.
6. Note whether "thinking" was on or off (it changes output length).
7. No other heavy jobs on the server during the run.
8. Save raw CSVs in [`results/`](results/) as `YYYY-MM-DD-<test>.csv`.

## Planned runs

| Test | Command (placeholders) |
| --- | --- |
| Single user | `bench_openai.py --base-url http://127.0.0.1:PORT/v1 --model MODEL --prompt-file prompts/short.txt --runs 5` |
| Prefill | same with `prompts/long.txt`, read engine timings |
| Web UI path TTFT | `--base-url https://AI_SERVER_HOSTNAME/api` with `BENCH_API_KEY` set |
| Concurrency | `--concurrency 3` and `--concurrency 10` |
