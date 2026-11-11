# Model Selection & Quantization

> Status: **Model: TBD** (see this document). No model has been chosen. Fill this in after the server is inventoried (M01) and the selection is recorded (M02 / M03).

## 1. Decision

| Field | Value |
| --- | --- |
| Model | TBD (see this document) |
| Repository / tag | TBD |
| Quant / exact file or tag | TBD |
| Licence (model card, date checked) | TBD |
| Context length | TBD |
| Parallel requests | TBD |

## 2. Selection criteria

A candidate must meet all of these before it is proposed. The team records the comparison in the table in §3; the teacher (and school IT where licence or safety is in question) accepts the choice as an ADR (M02).

1. **Fits the server's VRAM** once the GPU is inventoried in M01. The weights, the KV cache (which grows with context length × parallel requests) and driver overhead must fit on the GPU, or a documented CPU-offload trade-off is accepted.
2. **Licence allows school use.** The licence on the model card must permit use at a Norwegian upper-secondary school for teaching. Record the licence, a link to the card and the date checked. Flag any "research only", "no commercial use" or similar restriction for IT/the teacher.
3. **Norwegian + English quality.** The model should be usable for IM school work in Norwegian bokmål and in English. Note in the table if it is clearly weak in one of them.
4. **Safety / guardrails suitable for students.** Prefer an official release with normal safety behaviour. Refusal-removed, abliterated or "uncensored" models are **not planned**.

Do not treat a name in a draft pull request as a decision.

## 3. Candidate table

Leave rows empty until someone has actually checked the model card. Add a row per candidate (and, if useful, a separate row for a GGUF or Ollama build of the same model).

| Candidate | Repository / tag | Parameters | Licence (card, date checked) | Approx. weight size (quant) | Norwegian + English notes | Safety notes | Fits VRAM? | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

Status is one of: `research`, `rejected`, `proposed`, `chosen`.

## 4. How sizing and quantization work

Published "file size" is usually **weights only**. The GPU also needs memory for the KV cache and CUDA / driver overhead, so a file that is just under the VRAM number often will not fit once a useful context length is set.

Rough weight sizes (planning only, not a measurement):

| Precision / quant class | Approx. bytes per parameter | Example: 7B | Example: 27B | Example: 70B |
| --- | --- | --- | --- | --- |
| BF16 / FP16 | ~2 | ~14 GB | ~54 GB | ~140 GB |
| 8-bit (Q8_0 and similar) | ~1 | ~7 GB | ~27 GB | ~70 GB |
| 4-bit (Q4_K_M and similar) | ~0.5–0.65 | ~4–5 GB | ~15–18 GB | ~35–45 GB |
| Lower 3–4-bit (Q3, IQ4_XS, …) | smaller | smaller | smaller | smaller |

Rule of thumb, to be replaced by a real fit table after M01:

- Prefer the **largest quant that runs fully on the GPU** with the context length you need.
- If VRAM is tight, a smaller quant is usually better than heavy CPU offload (offload works, but it is much slower).
- Re-check sizes on the publisher's page (Hugging Face or Ollama) on the day you decide; community file lists change.
- After VRAM is known, fill the table below for the candidate you are evaluating (M03-004).

| File / tag | Quant | File size | Fits / tight / does not fit | Date checked | Source |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 5. Process

1. Inventory the GPU and VRAM (M01).
2. Add candidates to the table in §3 and check each against the criteria in §2, including the licence (M02).
3. Record the chosen model as an ADR (M02) and the exact file or tag as an ADR (M03).
4. Download only that file, verify the checksum, and fill in §6 (M09).

## 6. Deployed model (fill in after M09)

| Field | Value |
| --- | --- |
| Repository / tag | TBD |
| File | TBD |
| Size | TBD |
| SHA256 / Ollama digest | TBD |
| Downloaded on | TBD |
| VRAM used at configured context | TBD |

## 7. Switching models (M09-015)

TBD: exact steps (download, engine config, web UI model visibility), tested in M12.
