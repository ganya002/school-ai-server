# Model Selection & Quantization

> Status: **Planned.** The model actually deployed depends on the approval in M02 and on the GPU's VRAM (unknown, M01).

## 1. Candidate models (researched 2026-11-10)

| Role | Repository | Base | Licence (model card) |
| --- | --- | --- | --- |
| Requested ("Qwen 27B abliterated") | [`huihui-ai/Huihui-Qwen3.8-27B-abliterated`](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated) | `Qwen/Qwen3.8-27B` | Apache-2.0 |
| GGUF of the requested model | [`huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF`](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF) | — | — |
| Ollama tag of the requested model | [`huihui_ai/Qwen3.8-abliterated:27b-*`](https://ollama.com/huihui_ai/Qwen3.8-abliterated) (e.g. `27b-q4_K_M`) | — | — |
| Fallback (official) | [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) | — | Apache-2.0 |
| GGUF of the fallback | [`unsloth/Qwen3.8-27B-GGUF`](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF) | — | — |

Older abliterated generations also exist (e.g. `huihui-ai/Huihui-Qwen3.5-27B-abliterated`, `huihui-ai/Huihui-Qwen3.6-27B-abliterated-MTP-GGUF`). The plan targets the newest family at planning time (Qwen3.8; the official repository was created in August 2026). **Re-check before downloading** — community repositories change.

Model facts from the official card: 27B parameters, 64 layers, native context 262,144 tokens; "thinking" mode on by default and can be disabled per request. The repo is tagged image-text-to-text (a separate `mmproj` file adds vision in GGUF runtimes).

## 2. GGUF file sizes (from the Hugging Face file list, 2026-11-10)

| File (abliterated GGUF repo) | Size | Official equivalent (unsloth) | Size |
| --- | --- | --- | --- |
| `…-UD-IQ3_XXS.gguf` | 11.0 GB | `Qwen3.8-27B-UD-IQ3_XXS.gguf` | 10.9 GB |
| `…-UD-IQ4_XS.gguf` | 14.4 GB | `Qwen3.8-27B-UD-IQ4_XS.gguf` | 14.3 GB |
| `…-UD-DW-Q4_K_S.gguf` | 15.6 GB | `Qwen3.8-27B-UD-Q4_K_S.gguf` | 15.4 GB |
| `…-UD-DW-Q4_K_M.gguf` | 16.6 GB | `Qwen3.8-27B-UD-Q4_K_M.gguf` | 16.5 GB |
| `…-Q4_K.gguf` | 16.8 GB | — | |
| `…-UD-Q4_K_XL.gguf` | 17.4 GB | `Qwen3.8-27B-UD-Q4_K_XL.gguf` | 17.6 GB |
| `…-Q5_K.gguf` | 19.5 GB | `Qwen3.8-27B-UD-Q5_K_M.gguf` | 19.8 GB |
| `…-Q6_K.gguf` | 22.4 GB | `Qwen3.8-27B-UD-Q6_K.gguf` | 22.0 GB |
| `…-Q8_0.gguf` | 29.1 GB | `Qwen3.8-27B-Q8_0.gguf` | 29.1 GB |
| `…-bf16.gguf` | 54.7 GB | BF16 (2 parts) | 54.7 GB |
| `mmproj-model-bf16.gguf` (vision, optional) | 0.9 GB | `mmproj-BF16.gguf` | 0.9 GB |

Sizes are decimal GB as reported by the Hugging Face API. They are **file sizes only**: the GPU also needs memory for the KV cache (grows with context length × parallel requests) and CUDA overhead.

## 3. Rule of thumb for fit (verify in M03-004 and M09-009)

| VRAM | Likely choice | Notes |
| --- | --- | --- |
| < 16 GB | IQ3/IQ4_XS or partial CPU offload | Slower or lower quality. TBD |
| 24 GB | Q4_K_M / Q4_K_XL class (~16.5–17.5 GB) | Leaves ~5–6 GB for context/parallel slots |
| 32 GB | Q5/Q6 class or Q4 with long context | |
| 48 GB+ | Q8_0 | |

This table is a planning estimate, **not a measurement**. Record the real numbers in §5.

## 4. Decisions

| Decision | Value | ADR / issue |
| --- | --- | --- |
| Abliterated model approved | TBD | M02-003 |
| Primary model | TBD | M02-004 |
| Fallback model | `Qwen/Qwen3.8-27B` (proposed) | M02-004 |
| Quant / exact file or tag | TBD | M03-005 |
| Context length | TBD | M09-009 |
| Parallel requests | TBD | M09-010 |

## 5. Deployed model (fill in after M09)

| Field | Value |
| --- | --- |
| Repository / tag | TBD |
| File | TBD |
| Size | TBD |
| SHA256 / Ollama digest | TBD |
| Downloaded on | TBD |
| VRAM used at configured context | TBD |

## 6. Switching to the fallback model (M09-015)

TBD: exact steps (download, engine config, web UI model visibility), tested in M12-011.
