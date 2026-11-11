# Architecture

> Status: **Planned.** All components below are proposals until their ADR is accepted, except the OS: both nodes stay on Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)). Unknown values are `TBD`.

## 1. Context

Prosjekt 09 asks the team to get the school AI server running and make it available for IM students. **This team provides text-to-speech** (Norwegian + English); another group runs the LLM. The service must be reachable by remote admin access, act as a "Deployment Server" in security, host the TTS engines and have users with correct access.

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
| TTS engines | Main lineup in [tts-plan.md](tts-plan.md), each on `127.0.0.1` with `POST /v1/audio/speech` | Proposed (#26) | M02 / M09 |
| Model | TTS lineup (not an LLM) — see [model-selection.md](model-selection.md) | Proposed | #26 |
| Gateway | Voice picker / router in front of both nodes | Planned | M10 |
| Public HTTPS | **Default: Tailscale Funnel** (outbound only, no paid domain). Cloudflare named tunnel only if the school later provides a domain. Quick tunnels rejected. | Needs IT + teacher OK | M05 / M10 |
| Web UI | Optional; the required student path is the HTTPS API | Planned | M10 |
| Deployment server | Ansible control node + (optional) Wazuh — still waiting for clarification; Windows-compatible approach if in scope | TBD after clarification | M03-002, M11 |

WSL2 or Docker Desktop is **not** the default runtime. Use it only with Gabby's OK.

## 3. Data flows

1. Student or app, from any network → HTTPS (`https://tts-gateway.example-tailnet.ts.net`, placeholder) → Tailscale Funnel → gateway (API key, limits) → TTS engine on `127.0.0.1` (local or via the interconnect) → GPU or CPU.
2. Admin → private path (LAN / approved VPN / Tailscale admin) → SSH (key only) → Windows OpenSSH Server. SSH is not published on Funnel.
3. Deployment server → SSH → target machines (scope TBD).
4. Logs → Windows Event Log (retention per policy, no stored request text or audio by default) → optionally Wazuh.

## 4. Two-node layout

The service runs on **two PCs**, each on its existing Windows 11 install. The TTS lineup is split across nodes; one node runs the gateway and Funnel. Details are in [two-node-cluster.md](two-node-cluster.md) and [tts-plan.md](tts-plan.md).

## 5. Non-goals

- No inbound ports on the school router. Raw TTS ports and SSH stay private. The only planned public path is an outbound Tailscale Funnel in front of the gateway, after IT + teacher approval.
- No paid domain, and no third-party or company domain in this repo (placeholder: `https://tts-gateway.example-tailnet.ts.net`).
- No new hardware purchases are assumed.
- No model training or fine-tuning.
- No new operating system, dual boot, wipe, or partition.

## 6. Diagram

See the Mermaid diagram in the [README](../README.md#planned-architecture). Update it when ADRs are accepted (M03-015).
