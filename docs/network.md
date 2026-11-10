# Network & Port Matrix

> Status: **Planned.** Addresses are placeholders until IT says what may be committed.

## 1. Addressing

| Item | Value |
| --- | --- |
| Hostname | `AI_SERVER_HOSTNAME` (TBD) |
| IP / method | `AI_SERVER_IP` (static or DHCP reservation: TBD) |
| Network / VLAN | `SERVER_VLAN` (TBD) |
| Student network(s) | `STUDENT_NET_RANGE` (TBD) |
| Admin access range (VPN/Tailscale) | `ADMIN_VPN_RANGE` (TBD) |

## 2. Port matrix (draft, finalised in M03-012)

| Port | Service | Bound to | Allowed from | Reason |
| --- | --- | --- | --- | --- |
| 22/tcp | SSH | server interface / VPN interface | `ADMIN_VPN_RANGE` only | Admin access |
| 443/tcp | Web UI over HTTPS | server interface | `STUDENT_NET_RANGE`, `ADMIN_VPN_RANGE` | Students |
| 80/tcp | HTTP → HTTPS redirect (optional) | server interface | same as 443 | Redirect only |
| 8080/tcp (example) | Open WebUI backend | 127.0.0.1 if behind proxy | localhost | Internal |
| 11434/tcp (Ollama) / 8000 (vLLM) / 8080 (llama-server) | Inference API | **127.0.0.1** | localhost | Never exposed by default |
| TBD | Wazuh agent → manager (if in scope) | outbound | — | Deployment server |
| everything else | — | — | **denied** | Default deny |

No port is forwarded from the internet (verified in M06-003).

## 3. Firewall

Implemented with ufw ([Ubuntu docs](https://ubuntu.com/server/docs/how-to/security/firewalls)). See [`config/ufw/rules.example.md`](../config/ufw/rules.example.md).
