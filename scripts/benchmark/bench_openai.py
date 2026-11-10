#!/usr/bin/env python3
"""
Measure generation speed against an OpenAI-compatible chat completions endpoint
(Ollama /v1, llama.cpp llama-server /v1, vLLM /v1, or Open WebUI /api).

Standard library only. Uses streaming to measure time-to-first-token (TTFT) and
decode tokens/sec. Token counts come from the server's `usage` field when it is
sent; otherwise streamed chunks are counted (an approximation; noted in the CSV).

Example (on the server, engine on localhost):
  python3 bench_openai.py --base-url http://127.0.0.1:11434/v1 --model MODEL_ID \
      --prompt-file ../../benchmarks/prompts/short.txt --runs 5 --concurrency 1 \
      --out ../../benchmarks/results/$(date +%F)-single.csv

API keys: pass via the environment variable BENCH_API_KEY, never on the command line or in Git.
"""
import argparse, csv, json, os, statistics, sys, threading, time, urllib.request


def one_request(base_url, model, prompt, max_tokens, key, timeout):
    url = base_url.rstrip("/") + "/chat/completions"
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "stream": True, "stream_options": {"include_usage": True},
            "temperature": 0}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          **({"Authorization": f"Bearer {key}"} if key else {})})
    t0 = time.perf_counter(); ttft = None; chunks = 0; usage = None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                obj = json.loads(data)
            except ValueError:
                continue
            if obj.get("usage"):
                usage = obj["usage"]
            for ch in obj.get("choices") or []:
                d = ch.get("delta") or {}
                if d.get("content") or d.get("reasoning_content") or d.get("reasoning"):
                    if ttft is None:
                        ttft = time.perf_counter() - t0
                    chunks += 1
    total = time.perf_counter() - t0
    out_tokens = (usage or {}).get("completion_tokens") or chunks
    prompt_tokens = (usage or {}).get("prompt_tokens")
    decode_time = total - (ttft or 0)
    return {"ttft_s": round(ttft or total, 3), "total_s": round(total, 3),
            "completion_tokens": out_tokens, "prompt_tokens": prompt_tokens,
            "tokens_source": "usage" if usage and usage.get("completion_tokens") else "chunks",
            "decode_tok_s": round(out_tokens / decode_time, 2) if decode_time > 0 and out_tokens else None}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", required=True, help="e.g. http://127.0.0.1:11434/v1")
    ap.add_argument("--model", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--max-tokens", type=int, default=256)
    ap.add_argument("--runs", type=int, default=5, help="rounds; each round sends --concurrency requests")
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument("--warmup", type=int, default=1, help="unmeasured requests first (loads the model)")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--out", help="CSV file to append results to")
    a = ap.parse_args()
    key = os.environ.get("BENCH_API_KEY", "")
    prompt = open(a.prompt_file, encoding="utf-8").read()

    for _ in range(a.warmup):
        one_request(a.base_url, a.model, prompt, a.max_tokens, key, a.timeout)

    rows = []
    for rnd in range(1, a.runs + 1):
        results = [None] * a.concurrency
        def worker(i):
            try:
                results[i] = one_request(a.base_url, a.model, prompt, a.max_tokens, key, a.timeout)
            except Exception as e:  # record failures, do not hide them
                results[i] = {"error": str(e)[:200]}
        t0 = time.perf_counter()
        ts = [threading.Thread(target=worker, args=(i,)) for i in range(a.concurrency)]
        [t.start() for t in ts]; [t.join() for t in ts]
        wall = time.perf_counter() - t0
        ok = [r for r in results if "error" not in r]
        agg = round(sum(r["completion_tokens"] for r in ok) / wall, 2) if ok else None
        for i, r in enumerate(results):
            rows.append({"round": rnd, "request": i + 1, "concurrency": a.concurrency, "model": a.model,
                         "prompt_file": os.path.basename(a.prompt_file), "max_tokens": a.max_tokens,
                         "round_wall_s": round(wall, 3), "round_total_tok_s": agg, **r})
        print(f"round {rnd}: {len(ok)}/{a.concurrency} ok, aggregate {agg} tok/s", file=sys.stderr)

    ok = [r for r in rows if "error" not in r]
    if ok:
        dec = [r["decode_tok_s"] for r in ok if r.get("decode_tok_s")]
        ttft = [r["ttft_s"] for r in ok]
        print(json.dumps({"requests": len(rows), "errors": len(rows) - len(ok),
                          "median_decode_tok_s": statistics.median(dec) if dec else None,
                          "median_ttft_s": statistics.median(ttft),
                          "tokens_source": sorted({r["tokens_source"] for r in ok})}, indent=2))
    if a.out:
        fields = ["round", "request", "concurrency", "model", "prompt_file", "max_tokens", "round_wall_s",
                  "round_total_tok_s", "ttft_s", "total_s", "prompt_tokens", "completion_tokens",
                  "decode_tok_s", "tokens_source", "error"]
        new = not os.path.exists(a.out)
        with open(a.out, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            if new:
                w.writeheader()
            w.writerows(rows)
    return 0 if len(ok) == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
