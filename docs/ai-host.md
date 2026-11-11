# AI Host (Inference Engine)

> Status: **Planned.** This team runs **TTS engines**, not an LLM. The lineup, ports and Windows install notes are in [tts-plan.md](tts-plan.md). Both nodes run Windows 11 natively ([ADR 0001](../decisions/0001-windows-11-native.md)).

## 1. Engine comparison (to be completed in M03-006)

Prefer an engine that runs **natively on Windows 11**. WSL2 or Docker Desktop may be used only with Gabby's OK; they are not the default.

| | Ollama for Windows | llama.cpp `llama-server` (Windows) | vLLM |
| --- | --- | --- | --- |
| Model format | GGUF (via Ollama library or imported) | GGUF | Hugging Face safetensors, AWQ/GPTQ/FP8 etc. |
| School model available as | TBD (Ollama tag or imported GGUF) | GGUF files from the publisher | TBD (must fit the inventoried VRAM; see [model-selection.md](model-selection.md)) |
| OpenAI-compatible API | Yes ([docs](https://docs.ollama.com/openai)) | Yes ([README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)) | Yes ([docs](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)) |
| Concurrency | `OLLAMA_NUM_PARALLEL` | `--parallel` slots | Continuous batching (best throughput) |
| Install on Windows 11 | Official Windows app ([Windows docs](https://docs.ollama.com/windows)) | Official Windows/CUDA release or a documented Windows build ([build](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)) | Typically Linux or Docker; a weak default on native Windows 11 unless an approved exception is made |
| Open WebUI integration | Native | OpenAI connection | OpenAI connection |
| Ease for a student team | Easiest on Windows | Medium | Hardest, and poorly aligned with ADR 0001 |
| GPU needs | Flexible, partial CPU offload possible | Flexible, partial offload possible | Model must fit in VRAM |

Chosen: TBD (ADR).

## 2. Configuration (fill in after M09)

| Setting | Value |
| --- | --- |
| Engine + version | TBD |
| Install method | Native Windows (default). WSL2 / Docker Desktop only with Gabby's OK |
| Autostart | Windows service or Task Scheduler (not systemd) |
| Service / task name | TBD |
| Service account | TBD (a dedicated local account if needed) |
| Listen address | `127.0.0.1:PORT` |
| Model path | TBD (folder on an existing volume, e.g. `C:\AI\models`) |
| Model / tag | TBD |
| Context length | TBD |
| Parallel requests | TBD |
| Keep-alive | TBD |
| GPU/CPU split | TBD |

Windows-oriented examples: [`config/windows/ai-host-autostart.example.md`](../config/windows/ai-host-autostart.example.md). Older Linux systemd snippets under `config/ollama` and `config/llama-server` are not the plan.

## 3. Health checks

```powershell
Get-Service <engine-service>          # or a Task Scheduler task
nvidia-smi
# Ollama
curl.exe -s http://127.0.0.1:11434/api/tags
# llama.cpp (OpenAI-compatible)
curl.exe -s http://127.0.0.1:PORT/v1/models
```
