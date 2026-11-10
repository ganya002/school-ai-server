# AI Host (Inference Engine)

> Status: **Planned.** Engine choice in M03-007.

## 1. Engine comparison (to be completed in M03-006)

| | Ollama | llama.cpp `llama-server` | vLLM |
| --- | --- | --- | --- |
| Model format | GGUF (via Ollama library or imported) | GGUF | Hugging Face safetensors, AWQ/GPTQ/FP8 etc. |
| Requested model available as | `huihui_ai/Qwen3.8-abliterated:27b-*` | GGUF files from Hugging Face | `huihui-ai/Huihui-Qwen3.8-27B-abliterated` (BF16 ~55 GB; needs a quantized variant to fit typical VRAM) |
| OpenAI-compatible API | Yes ([docs](https://docs.ollama.com/openai)) | Yes ([README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)) | Yes ([docs](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)) |
| Concurrency | `OLLAMA_NUM_PARALLEL` | `--parallel` slots | Continuous batching (best throughput) |
| Install | Official script/package ([Linux](https://docs.ollama.com/linux)) | Prebuilt release or build ([build](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)) | Python/pip or Docker ([docs](https://docs.vllm.ai/en/latest/)) |
| Open WebUI integration | Native | OpenAI connection | OpenAI connection |
| Ease for a student team | Easiest | Medium | Hardest |
| GPU needs | Flexible, partial CPU offload possible | Flexible, partial offload possible | Model must fit in VRAM |

Chosen: TBD (ADR).

## 2. Configuration (fill in after M09)

| Setting | Value |
| --- | --- |
| Engine + version | TBD |
| Install method (native / Docker) | TBD |
| Service name | TBD |
| Service user | TBD |
| Listen address | `127.0.0.1:PORT` |
| Model path | TBD |
| Model / tag | TBD |
| Context length | TBD |
| Parallel requests | TBD |
| Keep-alive | TBD |
| GPU/CPU split | TBD |

Example service configuration: [`config/ollama/override.conf.example`](../config/ollama/override.conf.example), [`config/llama-server/llama-server.service.example`](../config/llama-server/llama-server.service.example).

## 3. Health checks

```bash
systemctl status <engine-service>
journalctl -u <engine-service> -n 100
nvidia-smi
# Ollama
curl -s http://127.0.0.1:11434/api/tags
# llama.cpp / vLLM (OpenAI-compatible)
curl -s http://127.0.0.1:PORT/v1/models
```
