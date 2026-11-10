# Architecture

> Status: **Planned.** All components below are proposals until their ADR is accepted. Unknown values are `TBD`.

## 1. Context

Prosjekt 09 asks the team to get the school AI server running and make it available for IM students. The server must be reachable by remote access, act as a "Deployment Server" in security, host the AI and have users with correct access.

| Fact | Value | Source |
| --- | --- | --- |
| Machine | TBD (which "school AI server") | M01-004 |
| Physical or VM | TBD | ADR (M03-003) |
| CPU / RAM | TBD / TBD | inventory |
| GPU / VRAM | TBD / TBD | inventory |
| Disk | TBD | inventory |
| Network segment | TBD | inventory/network-inventory.md |
| Expected users (total / peak concurrent) | TBD / TBD | M01-021 |

## 2. Components

| Layer | Component | Choice | Decided in |
| --- | --- | --- | --- |
| Hardware | Physical machine or Proxmox VM with PCI passthrough | TBD | M03-003 |
| OS | Ubuntu Server LTS | Version TBD | M03-008 |
| Remote access | OpenSSH (keys only) over school VPN / Tailscale / LAN | TBD | M03-010 |
| Host security | ufw, fail2ban, unattended-upgrades, journald, Lynis baseline | Planned | M06 |
| GPU | NVIDIA driver (Ubuntu packages), Container Toolkit only if Docker | Planned | M08 |
| Inference | Ollama / llama.cpp server / vLLM, bound to 127.0.0.1 | TBD | M03-007 |
| Model | Approved Qwen 27B variant, GGUF ~4-bit or larger | TBD | M02-003, M03-005 |
| Web UI | Open WebUI with roles, groups, banner, rate limit | Planned | M10 |
| TLS | School cert / internal CA / Tailscale HTTPS / reverse proxy | TBD | M06-014 |
| Deployment server | Ansible control node + (optional) Wazuh | TBD after clarification | M03-002, M11 |

## 3. Data flows

1. Student browser → HTTPS → (reverse proxy) → Open WebUI → inference engine on `127.0.0.1` → GPU.
2. Admin → private path (VPN/Tailscale/LAN) → SSH (key only) → server.
3. Deployment server → SSH → target machines (scope TBD).
4. Logs → journald (retention per policy) → optionally Wazuh.

## 4. Non-goals

- No public internet exposure.
- No new hardware purchases are assumed.
- No model training or fine-tuning.

## 5. Diagram

See the Mermaid diagram in the [README](../README.md#planned-architecture). Update it when ADRs are accepted (M03-015).
