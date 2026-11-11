# Architecture Decision Records (ADRs)

Important decisions are written down here so the team, the teacher and school IT can always see **what** was decided, **why**, and **who** decided it.

## How to add a decision

1. Copy [`0000-template.md`](0000-template.md) to `NNNN-short-title.md` using the next free number, e.g. `0001-physical-or-vm.md`.
2. Fill in every section. Write `TBD` rather than leaving blanks.
3. Set the status to **Proposed** and open a pull request linking the decision issue.
4. When the required people have approved it, set the status to **Accepted** and add it to the index.
5. Never delete an ADR. If a decision changes, write a new one and mark the old one **Superseded by NNNN**.

## Index

| # | Title | Status | Date | Responsible |
| --- | --- | --- | --- | --- |
| — | *(no decisions recorded yet)* | | | |

## Decisions expected during the project

| Decision | Milestone | Needs approval from |
| --- | --- | --- |
| Permission to use and reinstall the hardware | M01 | Teacher + IT |
| What infrastructure details may be committed | M01 | IT |
| Which model to run (and any conditions) | M02 | **Teacher + IT** |
| Node roles (web UI placement, backend split vs duplicate) | M15 / after M01 | Teacher |
| Private link between nodes (LAN + ufw, or WireGuard/Tailscale if IT allows) | M15 | IT |
| Logging: what is stored, who may read it; retention | M02 | Teacher + IT (privacy) |
| Rate limits / fair use | M02 | Teacher |
| Who may approve new models | M02 | Teacher |
| Meaning and scope of "Deployment Server" | M03 / M11 | Teacher |
| Physical install vs Proxmox VM | M03 | IT |
| Quantization / model file | M03 | — |
| Inference engine (Ollama / llama.cpp / vLLM) | M03 | — |
| OS version | M03 | IT |
| Native vs Docker per component | M03 | — |
| Remote access method | M03 | IT |
| Hostname and IP method | M03 | IT |
| Student account method (local / LDAP / SSO TBD) | M03 | IT |
| Secret store | M03 | IT |
| Disk layout and model path | M03 | — |
| TLS method for the web UI | M06 | IT |
| Automatic reboot policy | M06 | Teacher |
| Student shell access (default: none) | M07 | Teacher |
| NVIDIA driver hold | M08 | — |
| Where the Wazuh manager runs (if in scope) | M11 | IT |
| Backup scope and location | M14 | IT |
