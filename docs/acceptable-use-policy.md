# Acceptable Use Policy & Model Approval

> Status: **Draft — not approved.** The model choice, logging and rules on this page need written approval from the responsible teacher and school IT (milestone M02).

## 1. What is an "abliterated" model

An *abliterated* model is a community-modified version of an official model in which the internal "refusal direction" has been removed, so it no longer refuses requests that the original would refuse. It is sometimes called *uncensored*.

| | Official model | Abliterated candidate |
| --- | --- | --- |
| Repository | [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) | [`huihui-ai/Huihui-Qwen3.8-27B-abliterated`](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated) |
| Publisher | Qwen (Alibaba) | huihui-ai (community) |
| Refuses harmful requests | Yes (trained safety behaviour) | Largely no (refusals removed on purpose) |
| Licence declared on model card (checked 2026-11-10) | Apache-2.0 | Apache-2.0 |
| GGUF files | e.g. [`unsloth/Qwen3.8-27B-GGUF`](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF) | [`huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF`](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF), Ollama [`huihui_ai/Qwen3.8-abliterated`](https://ollama.com/huihui_ai/Qwen3.8-abliterated) |

The model card describes itself as "a crude, proof-of-concept implementation to remove refusals". Re-check the repository, version and licence before downloading (M02-005).

A system prompt or banner does **not** make an abliterated model safe; it only sets expectations.

## 2. Risks (to be completed in M02-002)

| # | Risk | Likelihood | Impact | Mitigation | Issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Harmful or illegal instructions are generated | TBD | High | Approval, AUP, logging, restricted groups, fallback model | M02-003 |
| 2 | Harassment / offensive content about classmates | TBD | High | AUP, reporting, account disable | M02-013 |
| 3 | Students rely on wrong answers | TBD | Medium | Banner, guide | M02-012 |
| 4 | Personal data typed into prompts | TBD | Medium | AUP, retention | M02-010 |
| 5 | Reputational risk for the school | TBD | High | Teacher/IT approval | M02-003 |
| 6 | One user monopolises the GPU | TBD | Low | Rate limits | M02-011 |
| … | | | | | |

## 3. Approval record

| Item | Decision | By | Date | Link |
| --- | --- | --- | --- | --- |
| Run abliterated model for IM students | TBD (approved / approved with conditions / not approved) | Teacher: TBD · IT: TBD | | |
| Conditions (e.g. teachers only, logging on) | TBD | | | |
| Fallback model | `Qwen/Qwen3.8-27B` (proposed) | | | |

## 4. Acceptable use policy for students (draft, Norwegian, version 0.1)

*Regler for bruk av skolens AI-server*

1. AI-serveren er for skolearbeid i IM-faget.
2. Ikke skriv inn personopplysninger om deg selv eller andre (navn, fødselsnummer, helse osv.).
3. Ikke bruk AI-en til å lage ulovlig, skadelig, trakasserende eller krenkende innhold.
4. AI-en kan ta feil. Sjekk viktige fakta selv.
5. Bruken logges slik skolen har bestemt (se punkt 5). <!-- TBD after M02-008 -->
6. Brudd på reglene kan føre til at kontoen stenges, og læreren blir informert.
7. Meld fra om feil eller skadelige svar til: TBD (rolle, ikke privat kontaktinfo).

Version: 0.1 (draft) · Approved by: TBD · Date: TBD

## 5. Logging and privacy (M02-008 – M02-010)

| Question | Answer |
| --- | --- |
| What is logged (prompts / answers / metadata) | TBD |
| Who may read logs | TBD |
| Retention for chats | TBD |
| Retention for system logs | TBD |
| School privacy requirements (personopplysningsloven / GDPR) | TBD, from school IT/privacy contact ([Lovdata](https://lovdata.no/dokument/NL/lov/2018-06-15-38), [Datatilsynet](https://www.datatilsynet.no/)) |

## 6. Banner and system prompt (M02-012)

- Banner text: TBD
- Default system prompt: TBD
- SSH login banner: TBD

## 7. Reporting misuse (M02-013)

TBD: who receives reports, how fast an account is disabled, when the teacher/IT is informed.
