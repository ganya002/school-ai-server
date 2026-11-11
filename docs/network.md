# Network & Port Matrix

> Status: **Planned.** Addresses are placeholders until IT says what may be committed.

## 1. Addressing

| Item | Value |
| --- | --- |
| Hostname | `AI_SERVER_HOSTNAME` (TBD; per-node names in the inventory) |
| IP / method | `AI_SERVER_IP` (static or DHCP reservation: TBD) |
| Network / VLAN | `SERVER_VLAN` (TBD) |
| Student network(s) | `STUDENT_NET_RANGE` (TBD) |
| Admin access range (VPN/Tailscale) | `ADMIN_VPN_RANGE` (TBD) |

## 2. Port matrix (draft, finalised in M03-012)

| Port | Service | Bound to | Allowed from | Reason |
| --- | --- | --- | --- | --- |
| 22/tcp | SSH (OpenSSH Server on Windows) | server interface / VPN interface | `ADMIN_VPN_RANGE` only | Admin access |
| 443/tcp | Web UI over HTTPS | server interface | `STUDENT_NET_RANGE`, `ADMIN_VPN_RANGE` | Students |
| 80/tcp | HTTP → HTTPS redirect (optional) | server interface | same as 443 | Redirect only |
| 8080/tcp (example) | Open WebUI backend | 127.0.0.1 if behind proxy | localhost | Internal |
| 11434/tcp (Ollama) / 8000 (vLLM) / 8080 (llama-server) | Inference API | **127.0.0.1** | localhost | Never exposed by default |
| TBD | Wazuh agent → manager (if in scope) | outbound | — | Deployment server |
| everything else | — | — | **denied** | Default deny |

No port is forwarded from the internet (verified in M06-003).

## 3. Firewall

Implemented with **Windows Defender Firewall** ([docs](https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/)). See [`config/windows-firewall/rules.example.ps1`](../config/windows-firewall/rules.example.ps1). Do not install ufw; both nodes run Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)).
