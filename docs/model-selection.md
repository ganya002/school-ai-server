# Model selection (TTS)

> Status: **Proposed TTS lineup** — confirm in GitHub issue #26. This team runs **text-to-speech** (Norwegian + English). Another group runs the LLM. See [tts-plan.md](tts-plan.md) for the full catalogue, rejected models, ports and access plan.

## 1. Decision

| Field | Value |
| --- | --- |
| Service | Text-to-speech gateway (OpenAI-compatible `POST /v1/audio/speech`) |
| Languages | Norwegian + English |
| Main lineup | Node B: VoxCPM2. Node A: Qwen3-TTS 12Hz 1.7B, Phonon 31M, Kokoro-82M. Both: Piper `no_NO` on CPU. |
| Confirmed? | Not yet (#26) |
| Public path | Tailscale Funnel after IT + teacher approval; placeholder `https://tts-gateway.example-tailnet.ts.net` |

There is no single "the model". Users pick a voice/model through the gateway. Licence-restricted catalogue items (Higgs Audio V3, Breeze TTS 2) are **research/demo only, not for the public school service**.

## 2. Selection criteria

A TTS candidate must meet these before it is proposed for the public school service:

1. **Fits the node's VRAM** (Node A: 16 GB discrete GPU only, iGPU does not add; Node B: 12 GB), or runs on CPU as a documented fallback (Piper).
2. **Licence allows school use** of a hosted service for teaching. Flag "research only", "non-commercial" or Llama-style extra terms. Those stay off the public service until a teacher/IT decision says otherwise.
3. **Norwegian and/or English** quality that matches its role (for example Piper as the instant Norwegian fallback, VoxCPM2 as the best NO+EN quality on 12 GB).
4. A **Windows 11 native** path (pip or an official Windows app). WSL2/Docker Desktop needs Gabby's OK and is not the default.

Do not treat a name in a draft pull request as a decision. Confirm the lineup in #26.

## 3. Where the table lives

The comparison, optional models, rejected models and links are in [tts-plan.md](tts-plan.md) (§2–§4). Do not duplicate that catalogue here.

## 4. Process

1. Inventory GPU and VRAM (M01) — in progress / done per node.
2. Confirm the lineup in #26 (M02). Teacher/IT must approve the public Funnel path before it goes live.
3. For each model: propose exact install commands in the issue, wait for Gabby's OK, install, benchmark (VRAM, time-to-first-audio, RTF), post results.
4. Record ports and the gateway mapping in [tts-plan.md](tts-plan.md) (placeholders only).

## 5. Deployed models (fill in after install)

| Model | Node | Version / tag | Port | VRAM | TTFA | RTF | Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |
