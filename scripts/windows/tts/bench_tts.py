#!/usr/bin/env python3
"""
Benchmark an OpenAI-compatible TTS endpoint (POST /v1/audio/speech returning WAV).

Standard library only. Per request it records:
  latency_s   wall time until the whole WAV arrived
  ttfa_s      time-to-first-audio: with --stream, time until the first PCM bytes after the WAV
              header arrive; without --stream it equals latency_s
  audio_s     length of the returned audio (from the WAV header)
  rtf         latency_s / audio_s   (below 1.0 = faster than real time)
  x_realtime  audio_s / latency_s   (the "audio duration / wall time" figure in docs/tts-plan.md)
Peak GPU memory is sampled with nvidia-smi every 200 ms while the run is going (if available).

Example (PowerShell, on the node, server on localhost):
  python bench_tts.py --base-url http://127.0.0.1:18101/v1 --model voxcpm2 --runs 5 --out C:\\tts\\out\\voxcpm2.csv

Test sentences are fixed below (no student data). API keys: env var BENCH_API_KEY, never on the command line.
"""
import argparse, csv, json, os, statistics, struct, subprocess, sys, threading, time, urllib.request

TEXTS = {
    "no": "Hei! Dette er en test av norsk talesyntese på skolens server. Været i dag er fint, og vi lærer om kunstig intelligens.",
    "en": "Hello! This is a test of English speech synthesis on the school server. Today we are learning about artificial intelligence.",
}


def vram_sampler(stop, peak):
    while not stop.is_set():
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                 capture_output=True, text=True, timeout=5).stdout
            peak[0] = max(peak[0], max(int(x) for x in out.split()))
        except Exception:
            return                        # no NVIDIA GPU / tool: leave peak at 0
        stop.wait(.2)


def one(base_url, model, voice, text, key, timeout, stream=False):
    body = json.dumps({"model": model, "input": text, "voice": voice, "response_format": "wav", "stream": stream}).encode()
    req = urllib.request.Request(base_url.rstrip("/") + "/audio/speech", data=body, method="POST",
                                 headers={"Content-Type": "application/json",
                                          **({"Authorization": f"Bearer {key}"} if key else {})})
    t0 = time.perf_counter(); ttfa = None; data = b""
    with urllib.request.urlopen(req, timeout=timeout) as r:
        while True:
            chunk = r.read1(65536) if hasattr(r, "read1") else r.read(65536)
            if not chunk:
                break
            data += chunk
            if ttfa is None and len(data) > 44:
                ttfa = time.perf_counter() - t0
    latency = time.perf_counter() - t0
    rate = struct.unpack("<I", data[24:28])[0]      # streamed WAV has no valid length field: count PCM bytes
    audio = (len(data) - 44) / 2 / rate
    return {"ttfa_s": round(ttfa if stream else latency, 3), "latency_s": round(latency, 3), "audio_s": round(audio, 3),
            "rtf": round(latency / audio, 3) if audio else None,
            "x_realtime": round(audio / latency, 2) if latency else None, "bytes": len(data)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", required=True, help="e.g. http://127.0.0.1:18101/v1")
    ap.add_argument("--model", required=True)
    ap.add_argument("--voice", default="default")
    ap.add_argument("--lang", choices=["no", "en", "both"], default="both")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--warmup", type=int, default=1)
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--stream", action="store_true", help="request streamed audio and measure real time-to-first-audio")
    ap.add_argument("--out", help="CSV file to append results to")
    a = ap.parse_args()
    key = os.environ.get("BENCH_API_KEY", "")
    langs = ["no", "en"] if a.lang == "both" else [a.lang]

    for _ in range(a.warmup):
        one(a.base_url, a.model, a.voice, TEXTS[langs[0]], key, a.timeout, a.stream)

    stop, peak = threading.Event(), [0]
    sampler = threading.Thread(target=vram_sampler, args=(stop, peak), daemon=True); sampler.start()
    rows = []
    for lang in langs:
        for run in range(1, a.runs + 1):
            try:
                r = one(a.base_url, a.model, a.voice, TEXTS[lang], key, a.timeout, a.stream)
            except Exception as e:        # record failures, do not hide them
                r = {"error": str(e)[:200]}
            rows.append({"model": a.model, "voice": a.voice, "lang": lang, "run": run, "stream": a.stream, **r})
            print(f"{lang} run {run}: {r}", file=sys.stderr)
    stop.set(); sampler.join(1)

    ok = [r for r in rows if "error" not in r]
    summary = {"requests": len(rows), "errors": len(rows) - len(ok), "peak_vram_mib": peak[0] or None}
    for lang in langs:
        L = [r for r in ok if r["lang"] == lang]
        if L:
            summary[lang] = {"median_ttfa_s": statistics.median(r["ttfa_s"] for r in L),
                             "median_latency_s": statistics.median(r["latency_s"] for r in L),
                             "median_rtf": statistics.median(r["rtf"] for r in L),
                             "median_x_realtime": statistics.median(r["x_realtime"] for r in L)}
    print(json.dumps(summary, indent=2))
    if a.out:
        fields = ["model", "voice", "lang", "run", "stream", "ttfa_s", "latency_s", "audio_s", "rtf", "x_realtime", "bytes", "error"]
        new = not os.path.exists(a.out)
        with open(a.out, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            if new:
                w.writeheader()
            w.writerows(rows)
    return 0 if len(ok) == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
