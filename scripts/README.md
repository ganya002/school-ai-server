# Scripts

| Script | What it does | Changes the system? |
| --- | --- | --- |
| [`linux/collect-hardware-inventory.sh`](linux/collect-hardware-inventory.sh) | Leftover Linux helper. Inventory on these nodes is done with read-only PowerShell ([ADR 0001](../decisions/0001-windows-11-native.md)) | No (read-only; not the plan) |
| [`benchmark/bench_openai.py`](benchmark/bench_openai.py) | Measures tokens/sec and time-to-first-token against an OpenAI-compatible endpoint | No |
| [`windows/tts/openai_tts_server.py`](windows/tts/openai_tts_server.py) | OpenAI-compatible `POST /v1/audio/speech` wrapper for one local TTS engine (VoxCPM2, Piper, or a `dummy` tone for testing clients); binds `127.0.0.1` | No (it is a server; installing its dependencies needs Gabby's OK) |
| [`windows/tts/bench_tts.py`](windows/tts/bench_tts.py) | Measures TTS latency, real-time factor and peak VRAM against `/v1/audio/speech` | No |
| [`windows/tts/tts_gateway.py`](windows/tts/tts_gateway.py) | **Draft** TTS gateway / voice picker (#250): per-student hashed API keys, rate limits, size limits, kill switch, routes `model` to a backend; stores no text or audio | No (it is a server; running it on a node needs Gabby's OK) |
| [`check-secrets.sh`](check-secrets.sh) | Scans the git diff for secrets and real IPs/MACs before a push | No |

None of the inventory or benchmark scripts have been run on the real servers yet. Run `check-secrets.sh` before every push.
