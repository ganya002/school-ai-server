# Architecture

> Status: **Planned.** All components below are proposals until their ADR is accepted, except the OS: both nodes stay on Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)). Unknown values are `TBD`.

## 1. Context

Prosjekt 09 asks the team to get the school AI server running and make it available for IM students. The server must be reachable by remote access, act as a "Deployment Server" in security, host the AI and have users with correct access.

| Fact | Value | Source |
| --- | --- | --- |
| Machines | Two PCs (Node A and Node B), already running Windows 11 | M01, ADR 0001 |
| Physical or VM | Physical machines; existing Windows 11, no hypervisor install | ADR 0001 |
| CPU / RAM | TBD / TBD | inventory |
| GPU / VRAM | TBD / TBD | inventory |
| Disk | Existing volumes only; do not repartition | inventory, ADR 0001 |
| Network segment | TBD | inventory/network-inventory.md |
| Expected users (total / peak concurrent) | TBD / TBD | M01-021 |

## 2. Components

| Layer | Component | Choice | Decided in |
| --- | --- | --- | --- |
| Hardware | The two existing physical PCs | Accepted | ADR 0001 |
| OS | Windows 11 as already installed (edition/build per inventory) | Accepted | ADR 0001 |
| Remote access | OpenSSH Server on Windows (keys only) over school VPN / Tailscale / LAN | TBD | M03-010 |
| Host security | Windows Defender Firewall, Windows Update, Event Log retention, Defender | Planned | M06 |
| GPU | Official NVIDIA driver on Windows; Container Toolkit only if Docker is later approved | Planned | M08 |
| Inference | Ollama for Windows or llama.cpp server (Windows), bound to 127.0.0.1; model TBD | TBD | M03-007 |
| Model | TBD (see [model-selection.md](model-selection.md)) | TBD | M02 (model decision), M03-005 |
| Web UI | Open WebUI with roles, groups, banner, rate limit, via a Windows-friendly method | Planned | M10 |
| TLS | School cert / internal CA / Tailscale HTTPS / reverse proxy | TBD | M06-014 |
| Deployment server | Ansible control node + (optional) Wazuh — still waiting for clarification; Windows-compatible approach if in scope | TBD after clarification | M03-002, M11 |

WSL2 or Docker Desktop is **not** the default runtime. Use it only with Gabby's OK.

## 3. Data flows

1. Student browser → HTTPS → (reverse proxy) → Open WebUI → inference engine on `127.0.0.1` → GPU.
2. Admin → private path (VPN/Tailscale/LAN) → SSH (key only) → Windows OpenSSH Server.
3. Deployment server → SSH → target machines (scope TBD).
4. Logs → Windows Event Log (retention per policy) → optionally Wazuh.

## 4. Two-node layout

The service runs on **two PCs**, each on its existing Windows 11 install. Roles (which node runs Open WebUI, whether backends are duplicated or split) are decided after both inventories. Details, placeholder addresses, health checks and the failover test list are in [two-node-cluster.md](two-node-cluster.md).

## 5. Non-goals

- No public internet exposure.
- No new hardware purchases are assumed.
- No model training or fine-tuning.
- No new operating system, dual boot, wipe, or partition.

## 6. Diagram

See the Mermaid diagram in the [README](../README.md#planned-architecture). Update it when ADRs are accepted (M03-015).
