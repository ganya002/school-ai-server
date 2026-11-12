# TTS plan

> Status: **Proposed lineup** (confirm in #26). This team's service is **text-to-speech** (Norwegian + English). Another group runs the LLM. Both nodes stay on Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)). Do not install anything on a live PC without Gabby's OK.

Students should be able to reach the gateway from **any network** (home, mobile hotspot, school), through an **outbound-only** tunnel. No inbound router ports are opened, and the team will **not** buy a domain.

## 1. What we are building

- Each node runs one or more TTS engines natively on Windows 11, each on `127.0.0.1` at its own port, exposing an OpenAI-compatible `POST /v1/audio/speech` so a client can pick a voice/model.
- A **gateway** on one node (which node is TBD) routes requests to the right backend and is the only process published through the tunnel.
- Backend APIs, SSH and internodal traffic stay off the public internet.

Install method: native Windows / `pip` in a venv. **WSL2 or Docker Desktop only with Gabby's OK, not the default.**

Neither VoxCPM2 nor Piper ships an OpenAI-compatible `/v1/audio/speech` server on Windows (VoxCPM2 has a Python API, CLI and Gradio demo; Piper's HTTP server uses `POST /synthesize`). Both are wrapped by [`scripts/windows/tts/openai_tts_server.py`](../scripts/windows/tts/openai_tts_server.py), one process per engine on its own `127.0.0.1` port. Benchmarks use [`scripts/windows/tts/bench_tts.py`](../scripts/windows/tts/bench_tts.py).

**Piper licence:** the maintained engine (`piper-tts`, [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl)) is **GPL-3.0-or-later**; the original MIT repo (rhasspy/piper) is archived. Running it as an internal service is fine (GPL, not AGPL). The Norwegian voices `no_NO-talesyntese-medium` (1 speaker) and `no_NO-nvcc-medium` (10 speakers) are **CC0** (Språkbanken data).

Node A is an RTX 5070 Ti (16 GB). That figure is the discrete GPU only: the iGPU's memory does **not** add to it. Before any PyTorch model on Node A, install a **cu128+** build and confirm `sm_120` is in `torch.cuda.get_arch_list()`.

## 2. Main lineup

These are the models we plan to install and benchmark first (VRAM, time-to-first-audio, real-time factor, short sample notes). Exact install commands go in the issue and wait for Gabby's OK.

| Model | Use it for | Node | VRAM (approx.) | Speed | Languages | Cloning | Licence | Install hint | Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VoxCPM2 | Best quality Norwegian + English on the 12 GB card | B (RTX 4070 Ti 12 GB) | ~8 GB | fast | Norwegian + English (and others) | Zero-shot, streaming | Apache 2.0 | `pip install voxcpm` | [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) |
| Qwen3-TTS 12Hz 1.7B | Near-ElevenLabs English, short clone | A (RTX 5070 Ti 16 GB) | ~6 GB | fast (~97 ms first packet; 3 s clone) | English (card also lists other languages; Norwegian is not the reason we pick it) | 3 s clone | Apache 2.0 | `pip install -U qwen-tts` (no FlashAttention on Windows) | [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) |
| Phonon 31M | Instant English replies | A | low (31M) | instant | English | No (preset / model card) | Apache 2.0 | `pip install ptts` (ships an OpenAI-compatible server) | [gradium/phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en) |
| Kokoro-82M | Extra English preset voices | A | low (82M) | instant / fast | English | Preset voices | Apache 2.0 | [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) `start-gpu.ps1` | [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) · [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) |
| Piper `no_NO` | Instant Norwegian fallback, CPU | **Both** (CPU) | CPU (almost no VRAM) | instant | Norwegian | Preset voices | Engine GPL-3.0-or-later (`piper-tts`); voices CC0 | Piper + [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices) `no_NO` | [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices) |

## 3. Model catalogue

A larger menu so the team can see what each option is for. **Speed tier:** instant / fast / slow-quality. Licence-restricted models are flagged as **research/demo only, not for the public school service**. Links below were checked and returned HTTP 200 on 2026-11-11. Official Higgs Audio V3 weight pages on Hugging Face returned 401 and are not used as links.

| Model | Best for | Node | VRAM | Speed tier | Languages | Cloning | Licence | Link |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VoxCPM2 | Best quality Norwegian + English we can run on 12 GB | B | ~8 GB | fast | Norwegian + English | Zero-shot, streaming | Apache 2.0 | [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) |
| Qwen3-TTS 12Hz 1.7B | High-quality English, short clone, low first-packet latency | A | ~6 GB | fast | English (plus other card languages) | 3 s clone | Apache 2.0 | [Qwen/Qwen3-TTS-12Hz-1.7B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base) |
| Qwen3-TTS 12Hz 0.6B | Lighter Qwen3 English when 1.7B is tight | A (or B) | lower than 1.7B | fast | English (plus other card languages) | Yes (same family) | Apache 2.0 | [Qwen/Qwen3-TTS-12Hz-0.6B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) |
| Phonon 31M | Instant English, tiny footprint | A | very low | instant | English | No (lightweight English model) | Apache 2.0 | [gradium/phonon-31m-en](https://huggingface.co/gradium/phonon-31m-en) |
| Kokoro-82M | Instant English preset voices | A | very low | instant | English | Preset voices | Apache 2.0 | [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) · [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) |
| Piper `no_NO` | Instant Norwegian fallback on CPU | Both (CPU) | CPU | instant | Norwegian | Preset voices | Engine GPL-3.0-or-later; voices CC0 | [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices) |
| Ming-3.0-tts-0.5B | Slow-but-excellent English that still fits 12/16 GB; strong blind-test score in this size | A or B | fits 12/16 GB (measure) | slow-quality | English (also zh and others; we would use it for English) | Zero-shot + voice design | MIT | [inclusionAI/Ming-3.0-tts-0.5B](https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B) |
| Orpheus 3B | Expressive / emotional English | A (16 GB preferred) | ~3B class (measure) | fast / slow-quality (measure) | English | Zero-shot; emotion tags | Llama-based terms for the weights (repo code Apache 2.0) — confirm before any public use | [canopylabs/orpheus-3b-0.1-ft](https://huggingface.co/canopylabs/orpheus-3b-0.1-ft) |
| Sesame CSM-1B | Conversational English with dialogue context | A or B | ~1B class (measure) | fast (measure) | English | Conversational context | Apache 2.0 | [sesame/csm-1b](https://huggingface.co/sesame/csm-1b) |
| Dia 1.6B / Dia2 | Two-speaker dialogue, podcasts, laugh/sigh tags | A or B | 1.6B / 2B class (measure) | fast (measure) | English | Multi-speaker scripts | Apache 2.0 | [Dia-1.6B](https://huggingface.co/nari-labs/Dia-1.6B) · [Dia2-2B](https://huggingface.co/nari-labs/Dia2-2B) · [dia](https://github.com/nari-labs/dia) · [dia2](https://github.com/nari-labs/dia2) |
| Kyutai Pocket TTS | CPU voice cloning, very low latency (~200 ms) | Either (CPU/GPU) | CPU-friendly | instant | English (card also lists other languages) | Yes, on CPU | CC-BY-4.0 | [kyutai/pocket-tts](https://huggingface.co/kyutai/pocket-tts) |
| Kyutai TTS 1.6B | Streaming English (and French) | A or B | ~1.6B (measure) | fast / streaming | English, French | Per card | CC-BY-4.0 | [kyutai/tts-1.6b-en_fr](https://huggingface.co/kyutai/tts-1.6b-en_fr) |
| Higgs Audio V3 | Top-tier quality English, **not for the public school service** | — | measure if ever demoed | slow-quality | English | Per card | **Research/demo only, not for the public school service** (vendor licence `other`). Official bosonai weight pages were not publicly resolvable (HTTP 401) on 2026-11-11. | Public community port: [multimodalart/higgs-audio-v3-tts-4b-transformers](https://huggingface.co/multimodalart/higgs-audio-v3-tts-4b-transformers) · [higgs-audio](https://github.com/boson-ai/higgs-audio) |
| Breeze TTS 2 | Top-tier quality, **not for the public school service** | — | measure if ever demoed | slow-quality | English, Chinese | Per card | **Research/demo only, not for the public school service** (`breezeblue-research-and-non-commercial-license`) | [BreezeBlue/Breeze-TTS-2](https://huggingface.co/BreezeBlue/Breeze-TTS-2) |

Qwen 0.6B, Kyutai models, Higgs and Breeze are **catalogue-only** (no install issue unless a later decision says otherwise). Ming, Orpheus, Dia and CSM have optional issues only.

## 4. Rejected (with reason)

| Model | Why not |
| --- | --- |
| Fish Audio Drama 3 | About 48 GB VRAM, and the licence bans a hosted service |
| XTTS-v2, F5-TTS, Fish S1 | Non-commercial / not usable for the public school service |
| VibeVoice | Pulled |
| Chatterbox | Retired |

## 5. Placeholder ports

Do not commit real IPs. Each engine listens on `127.0.0.1` only. The gateway (TBD which node) is the process published through Tailscale Funnel, on a Funnel-allowed port (443, 8443 or 10000).

| Service | Node | Bind | Port (placeholder) |
| --- | --- | --- | --- |
| Qwen3-TTS 1.7B | A | `127.0.0.1` | 18001 |
| Phonon 31M | A | `127.0.0.1` | 18002 |
| Kokoro-FastAPI | A | `127.0.0.1` | 18003 |
| Piper `no_NO` | A | `127.0.0.1` | 18004 |
| VoxCPM2 | B | `127.0.0.1` | 18101 (installed 2026-11-11, #240) |
| Piper `no_NO` | B | `127.0.0.1` | 18102 (installed 2026-11-11, #245) |
| Gateway / voice picker | TBD | localhost, Funnel in front | 443, 8443 or 10000 |

Record the final mapping here once it is decided. Health checks and interconnect allowlists use these placeholders only.

## 6. Public access (outbound-only tunnel)

**Default: Tailscale Funnel.** No paid domain. Students should not need a Tailscale client. The stable URL looks like `https://<machine>.<tailnet>.ts.net`. In this repo use only the placeholder:

`https://tts-gateway.example-tailnet.ts.net`

Never write a real tailnet, machine name, domain or token in this public repository.

How it should work (only after school IT + teacher approval, and Gabby's OK to install):

1. Install [Tailscale for Windows](https://tailscale.com/download/windows) as a service on the **gateway** node.
2. Publish the gateway with `tailscale funnel` on the chosen Funnel port. Funnel only serves **443, 8443 and 10000**, and it has **bandwidth limits** — read the current official notes before going live: [Tailscale Funnel](https://tailscale.com/docs/features/tailscale-funnel) and [`tailscale funnel`](https://tailscale.com/docs/reference/tailscale-cli/funnel).
3. The node makes an **outbound-only** connection. Do **not** open inbound ports on the school router.
4. Students call `POST https://tts-gateway.example-tailnet.ts.net/v1/audio/speech` with a per-student API key (see [client-guide.md](client-guide.md)).

**If the school later provides a domain:** a Cloudflare **named** tunnel (`cloudflared` as a Windows service, HTTPS only) may be considered. That is not the default, and it still needs IT approval.

**Rejected:** Cloudflare quick tunnels (`trycloudflare.com`). The URL changes on every restart, so it is not usable as a school service.

Admin SSH stays on the private path (LAN / approved VPN / Tailscale SSH if IT allows it). Funnel must not publish SSH or raw backend ports.

## 7. Security on the gateway

Must be in place before the tunnel is turned on for students:

- A **per-student API key** on every request (`Authorization: Bearer …`). No key, no audio.
- **Rate limits and quotas** per key (requests and generated audio).
- **Request size limits** (text length and upload size).
- An **abuse / kill switch** that can disable a key or the whole public path quickly.
- **Do not store** request text or generated audio (beyond short-lived processing in memory). Logging stays within the privacy ADR (M02): no content dumps in this repo or on disk by default.

Windows Defender Firewall stays default-deny for inbound LAN/internet traffic. Funnel traffic is outbound from the node.

## 8. Benchmarks

For each installed model, post in the issue (placeholders only):

- Peak VRAM (`nvidia-smi`)
- Time-to-first-audio
- Real-time factor (audio duration / wall time)
- Short notes on a Norwegian and/or English sample (no student recordings)

### Node B results (2026-11-11)

Measured with [`bench_tts.py`](../scripts/windows/tts/bench_tts.py): 5 runs per language after one warm-up, non-streaming, so latency = time-to-first-audio. RTF = latency / audio (below 1 = faster than real time). Raw CSVs are in [`benchmarks/results/`](../benchmarks/results/).

| Engine (Node B) | Versions | Median latency NO / EN | RTF | VRAM | Notes |
| --- | --- | --- | --- | --- | --- |
| VoxCPM2 | voxcpm 2.0.3, torch 2.8.0+cu128, `optimize=False` | 13.1 s / 14.8 s | 2.05 | ~5.2 GB loaded, 5.6 GB peak | 2x slower than real time without `torch.compile`; speed-up options in #240 |
| Piper `no_NO-talesyntese-medium` | piper-tts 1.8.0, onnxruntime 1.31.1 (CPU) | 0.97 s / 1.13 s | 0.15 | ~0 (CPU) | `nvcc` voice: RTF 0.16 |

Listening notes are still TBD (a human must listen to the samples).

## 9. Related issues

- Confirm lineup: [#26](https://github.com/ganya002/school-ai-server/issues/26)
- Main: [#241](https://github.com/ganya002/school-ai-server/issues/241) Qwen3-TTS (A), [#242](https://github.com/ganya002/school-ai-server/issues/242) Phonon (A), [#243](https://github.com/ganya002/school-ai-server/issues/243) Kokoro (A), [#244](https://github.com/ganya002/school-ai-server/issues/244) Piper (A), [#240](https://github.com/ganya002/school-ai-server/issues/240) VoxCPM2 (B), [#245](https://github.com/ganya002/school-ai-server/issues/245) Piper (B)
- Optional: [#246](https://github.com/ganya002/school-ai-server/issues/246) Ming (A), [#247](https://github.com/ganya002/school-ai-server/issues/247) Orpheus (A), [#249](https://github.com/ganya002/school-ai-server/issues/249) CSM (A), [#248](https://github.com/ganya002/school-ai-server/issues/248) Dia/Dia2 (B)
- Both: [#250](https://github.com/ganya002/school-ai-server/issues/250) voice picker / router, [#251](https://github.com/ganya002/school-ai-server/issues/251) public HTTPS via Tailscale Funnel (needs IT OK)

## 10. Related documents

- [client-guide.md](client-guide.md) — how a student or app calls the gateway
- [two-node-cluster.md](two-node-cluster.md)
- [security-hardening.md](security-hardening.md)
- [model-selection.md](model-selection.md)
- [ai-host.md](ai-host.md)
