#!/usr/bin/env python3
"""
TTS gateway / voice picker (DRAFT, #250). The only process that Tailscale Funnel should publish.

Routes POST /v1/audio/speech to the backend that serves the requested `model`
(openai_tts_server.py on Node A or Node B), and enforces on every request:
  - a per-student API key (Authorization: Bearer ...), stored only as a SHA-256 hash
  - per-key rate limit (requests/minute) and daily character quota
  - request size limits (body bytes and input characters)
  - kill switches: a file named KILL next to the keys file stops all traffic (503);
    "disabled": true on a key stops that key. Both are re-read on every request.
  - no storage: request text and audio are never logged or written to disk

Endpoints:
  GET  /health            gateway status (no key needed, no details)
  GET  /v1/models         models and voices the key may use
  POST /v1/audio/speech   OpenAI-compatible; "stream": true is passed through

Files (examples in config/tts-gateway/):
  backends.json  {"models": {"voxcpm2": {"url": "http://127.0.0.1:18101", "voices": [...], "languages": [...]}}}
  keys.json      {"<sha256 of key>": {"label": "student-01", "rpm": 10, "chars_per_day": 20000, "disabled": false}}

Make a key (prints the secret once; store only the hash line in keys.json):
  python tts_gateway.py --new-key student-01

Run (PowerShell, gateway node; localhost only, Funnel sits in front):
  python tts_gateway.py --backends C:\\tts\\gateway\\backends.json --keys C:\\tts\\gateway\\keys.json --port 18080

Needs: fastapi, uvicorn (standard library for the proxying).
"""
import argparse, collections, hashlib, http.client, json, secrets, sys, threading, time
from pathlib import Path
from urllib.parse import urlsplit

MAX_BODY = 16 * 1024      # bytes
MAX_CHARS = 1000          # characters of input text per request


def sha(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


class Keys:
    """keys.json, re-read when it changes on disk, so revoking a key needs no restart."""
    def __init__(self, path):
        self.path, self.mtime, self.data = Path(path), None, {}
    def get(self, key):
        m = self.path.stat().st_mtime
        if m != self.mtime:
            self.data, self.mtime = json.loads(self.path.read_text(encoding="utf-8")), m
        return self.data.get(sha(key))


class Limits:
    # ponytail: in-memory counters reset on restart; persist them if a restart-to-reset loophole matters.
    def __init__(self):
        self.lock = threading.Lock()
        self.hits = collections.defaultdict(collections.deque)   # key hash -> request times (last 60 s)
        self.chars = collections.defaultdict(int)                 # (key hash, day) -> characters used
    def check(self, h, rpm, chars_per_day, n):
        now, day = time.time(), time.strftime("%Y-%m-%d")
        with self.lock:
            q = self.hits[h]
            while q and now - q[0] > 60:
                q.popleft()
            if len(q) >= rpm:
                return "rate limit: too many requests per minute"
            if self.chars[(h, day)] + n > chars_per_day:
                return "daily character quota used up"
            q.append(now); self.chars[(h, day)] += n
        return None


def build_app(backends, keys, kill_file):
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import JSONResponse, StreamingResponse
    from starlette.concurrency import run_in_threadpool

    app = FastAPI(title="TTS gateway", docs_url=None, redoc_url=None, openapi_url=None)
    limits = Limits()

    def auth(request: Request):
        if kill_file.exists():
            raise HTTPException(503, "service paused by admin")
        h = request.headers.get("authorization", "")
        if not h.lower().startswith("bearer "):
            raise HTTPException(401, "missing API key")
        k = keys.get(h[7:].strip())
        if not k or k.get("disabled"):
            raise HTTPException(401, "invalid or disabled API key")
        return sha(h[7:].strip()), k

    @app.get("/health")
    def health():
        return {"status": "paused" if kill_file.exists() else "ok"}

    @app.get("/v1/models")
    def models(request: Request):
        auth(request)
        return {"object": "list", "data": [{"id": m, "object": "model", "owned_by": "school",
                                            "voices": b.get("voices", []), "languages": b.get("languages", [])}
                                           for m, b in backends.items()]}

    @app.post("/v1/audio/speech")
    async def speech(request: Request):
        h, k = auth(request)
        body = await request.body()
        if len(body) > MAX_BODY:
            raise HTTPException(413, "request too large")
        try:
            req = json.loads(body)
        except ValueError:
            raise HTTPException(400, "body must be JSON")
        text, model = req.get("input"), req.get("model")
        if not isinstance(text, str) or not text.strip():
            raise HTTPException(400, "'input' must be non-empty text")
        if len(text) > MAX_CHARS:
            raise HTTPException(413, f"'input' is longer than {MAX_CHARS} characters")
        if model not in backends:
            raise HTTPException(404, "unknown model; see GET /v1/models")
        err = limits.check(h, k.get("rpm", 10), k.get("chars_per_day", 20000), len(text))
        if err:
            raise HTTPException(429, err)

        # forward only known fields to the backend
        fwd = {f: req[f] for f in ("model", "input", "voice", "response_format", "speed", "stream", "stream_format") if f in req}
        u = urlsplit(backends[model]["url"])
        conn = http.client.HTTPConnection(u.hostname, u.port, timeout=300)
        def send():
            conn.request("POST", "/v1/audio/speech", json.dumps(fwd).encode(), {"Content-Type": "application/json"})
            return conn.getresponse()
        try:
            resp = await run_in_threadpool(send)      # blocking I/O off the event loop
        except OSError:
            conn.close()
            raise HTTPException(502, f"backend for '{model}' is not reachable")
        if resp.status != 200:
            detail = resp.read(2000).decode("utf-8", "replace"); conn.close()
            return JSONResponse({"error": "backend error", "status": resp.status, "detail": detail}, status_code=502 if resp.status >= 500 else resp.status)

        def relay():
            try:
                while chunk := resp.read1(65536):
                    yield chunk
            finally:
                conn.close()
        return StreamingResponse(relay(), media_type=resp.getheader("Content-Type", "audio/wav"))

    return app


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--new-key", metavar="LABEL", help="print a new random key and its keys.json entry, then exit")
    ap.add_argument("--backends", help="backends.json")
    ap.add_argument("--keys", help="keys.json (hashed keys)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=18080)
    a = ap.parse_args()
    if a.new_key:
        key = "tts_" + secrets.token_urlsafe(24)
        print(f"API key (give to the student once, never commit it): {key}")
        print("keys.json entry:", json.dumps({sha(key): {"label": a.new_key, "rpm": 10, "chars_per_day": 20000, "disabled": False}}))
        return
    if not (a.backends and a.keys):
        ap.error("--backends and --keys are required")
    backends = json.loads(Path(a.backends).read_text(encoding="utf-8"))["models"]
    keys = Keys(a.keys)
    keys.get("")                          # fail fast if keys.json is missing or invalid
    import uvicorn
    uvicorn.run(build_app(backends, keys, Path(a.keys).with_name("KILL")), host=a.host, port=a.port, access_log=False)


if __name__ == "__main__":
    sys.exit(main())
