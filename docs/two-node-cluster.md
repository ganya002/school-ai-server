# Two-node cluster (Node A and Node B)

> Status: **Planned.** Two PCs will run as one school AI service. **Roles are TBD** until both machines are inventoried in M01. All addresses below are placeholders, not real school IPs.

The two machines are:

| | Node A | Node B |
| --- | --- | --- |
| Human owner | Gabby | Gabby's friend |
| Coding agent | DeepSeek | Claude |
| Inventory | [hardware-inventory.md](../inventory/hardware-inventory.md#node-a) | [hardware-inventory.md](../inventory/hardware-inventory.md#node-b) |
| Hostname (placeholder) | `AI_NODE_A_HOSTNAME` | `AI_NODE_B_HOSTNAME` |
| IPv4 (placeholder) | `192.0.2.10` | `192.0.2.11` |

Agents coordinate only through this repository and GitHub issues. See [AGENTS.md](../AGENTS.md).

## 1. How the two PCs talk

- Both nodes sit on the **same school LAN / VLAN** (record the segment, or a placeholder, in [network-inventory.md](../inventory/network-inventory.md)).
- Each node gets a **static address or a DHCP reservation**, written here only as a placeholder until IT allows otherwise (`192.0.2.10` / `192.0.2.11`).
- They trust each other over **SSH keys** (one key pair per admin, plus a dedicated interconnect key if useful). Password SSH stays off.
- **Private link:** prefer the plain school LAN, with `ufw` on each node allowing only the other node's address on the interconnect ports (SSH from admins, and the inference API only from the node that runs the proxy). Use **WireGuard or Tailscale only if school IT allows it**. If they do, the allowlist uses the overlay addresses instead of (or as well as) the LAN addresses. If they do not, do not install an overlay VPN.
- Nothing on either node is forwarded from the public internet.

## 2. Roles (decision after both M01 inventories)

Pick one of these once CPU, RAM, GPU and VRAM are known for **both** PCs. Record the choice as an ADR. Until then, do not install a "primary" that the other node cannot actually support.

| Option | When to use | What runs where |
| --- | --- | --- |
| **A. Shared web UI, two backends** (default proposal) | Both nodes can run the chosen model (or a chosen quant of it) | Each node runs its own inference backend, bound to localhost or to the other node only. **One** node runs Open WebUI and a reverse proxy that load-balances or fails over to both backends over the OpenAI-compatible API. |
| **B. Model split** | VRAM (or licence/quality needs) differ a lot | Each node runs a different model or quant. The web UI lists both; users pick a model, or a lightweight router sends a request type to a given node. Failover is limited (the other model is not a copy). |
| **C. Active / spare** | One node is clearly weaker | The stronger node serves all traffic; the other is a warm spare with the same model, used only if the first backend fails. |

Proposed default, to confirm after inventory: **option A**, with Open WebUI + the reverse proxy on Node A unless Node B is the better place for that (disk, RAM, or network reachability from students).

Shared configuration (example systemd units, ufw rules, Open WebUI env, proxy snippets) lives in this repo as `*.example` files. Each node applies the same patterns with its own placeholders. Do not copy real secrets into the repo.

## 3. Ports (placeholders)

| Service | Listen on | Who may connect |
| --- | --- | --- |
| SSH | each node, port 22 (or the decided SSH port) | Admin path only (M05), plus the other node if interconnect SSH is wanted |
| Inference API | `127.0.0.1` and/or the other node, OpenAI-compatible port TBD | The proxy / Web UI node only, never students directly, never the internet |
| Open WebUI / HTTPS | the UI node, 443 (TLS method TBD) | Students and staff on the approved school path |
| WireGuard / Tailscale | only if IT approved | The two nodes (and approved admins) |

Exact numbers go in [docs/network.md](network.md) when the port matrix is decided (M03).

## 4. SSH trust

1. Each node has key-only SSH, no root login, `AllowGroups` as in the hardening examples.
2. The two human owners can SSH to **their** node from the approved admin path.
3. Interconnect: Node A can run a limited, key-only SSH command on Node B (and the other way around) if operations need it (health checks, controlled restarts). Use a dedicated key and a `forced-command` or a narrow sudoers rule when that is set up. Until then, humans SSH to their own node only.
4. Host keys are recorded out of band (not as real keys in this public repo).

## 5. Health checks and time sync

Both nodes use `Europe/Oslo` and the same NTP source (or a public NTP pool if IT has no internal one). Clock skew should stay well under a second.

Health checks (run on each node, and from the proxy to each backend):

```bash
# Time
timedatectl status
# From A, replace placeholders:
# ping -c 3 192.0.2.11
# ssh -o BatchMode=yes aiadmin@192.0.2.11 'echo ok && date --iso-8601=seconds'
# curl -sS --max-time 5 http://192.0.2.11:PORT/v1/models
```

The inference check must use the address and port that the firewall actually allows, not a public URL. Record the exact commands here once they are decided (M15).

The reverse proxy or Open WebUI should treat a backend as down when the health check fails, and send new requests to the remaining backend (option A or C).

## 6. Test checklist (A↔B connectivity and failover)

Run this in M15 after both OS installs and both AI hosts are up. Attach evidence to the test issue. Use placeholders in anything committed to Git.

- [ ] Node A and Node B have reserved/static placeholder addresses documented, and IT has confirmed they are on the same LAN/VLAN.
- [ ] From A, the interconnect path to B works (ping or equivalent, then SSH if interconnect SSH is in scope).
- [ ] From B, the same path back to A works.
- [ ] Time on A and B is in sync (`timedatectl` on both; skew recorded).
- [ ] `ufw` on each node allows the other node only on the agreed ports; a test from a third address on a non-allowed port is refused.
- [ ] Each backend answers `/v1/models` (or the engine's health URL) from the proxy node.
- [ ] A chat request through the web UI is served successfully.
- [ ] **Failover:** stop the inference service on one node. A new chat request still succeeds on the other backend (option A or C) or fails clearly for a model that only lived on the stopped node (option B). Record how long it takes.
- [ ] Start the stopped service again; both backends show healthy.
- [ ] Repeat the failover test in the other direction.
- [ ] Confirm neither inference port nor SSH answers from the public internet (IT or an off-site check, as in M06).

## 7. Related documents

- [architecture.md](architecture.md) — overall design
- [network.md](network.md) — port matrix
- [remote-access.md](remote-access.md) — SSH and admin path
- [security-hardening.md](security-hardening.md) — ufw, fail2ban
- [ai-host.md](ai-host.md) — inference engines
- [web-ui-and-api.md](web-ui-and-api.md) — Open WebUI
- [acceptance-checklist.md](acceptance-checklist.md)
