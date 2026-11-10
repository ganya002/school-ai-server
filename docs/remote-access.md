# Remote Access

> Status: **Planned.** The access method is decided in M03-010. **The server is never exposed to the public internet.**

## 1. Requirements

| Scenario | Needed? | Method |
| --- | --- | --- |
| Admins on the school network | Yes | SSH over the admin path |
| Admins off-site | TBD (M01-018) | School VPN / Tailscale / WireGuard (TBD) |
| Students on the school network | Yes (web UI only) | HTTPS |
| Students off-site | TBD (M01-018) | TBD, only through an approved private path |

## 2. SSH policy

- Keys only (`PasswordAuthentication no`, `KbdInteractiveAuthentication no`).
- No root login (`PermitRootLogin no`).
- Only groups `ai-admins` and `ai-operators` (`AllowGroups`).
- Personal ed25519 keys with passphrases; private keys never leave the owner's device.
- fail2ban sshd jail.

Example drop-in: [`config/ssh/10-hardening.conf.example`](../config/ssh/10-hardening.conf.example). Always validate with `sudo sshd -t` and keep a second session open before restarting.

## 3. Private access path (M03-010, M05-006)

| Option | Notes |
| --- | --- |
| School VPN | Preferred if available; IT manages it |
| Tailscale | Needs IT approval (external coordination service). Restrict with ACLs ([docs](https://tailscale.com/kb/1018/acls)) |
| WireGuard | Self-hosted; needs a reachable endpoint, which may require IT changes |
| LAN only | Simplest; no off-site access |

Chosen: TBD.

## 4. Emergency / console access (M05-009)

| Path | Who | Tested |
| --- | --- | --- |
| Proxmox web console (VM path) | TBD | TBD |
| Physical keyboard/monitor (physical path) | TBD | TBD |
| BMC/IPMI (if present) | TBD | TBD |

## 5. Client config example

```sshconfig
Host ai-server
    HostName AI_SERVER_HOSTNAME
    User YOUR_USERNAME
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

## 6. Adding / removing an admin key

See [users-and-roles.md](users-and-roles.md#onboarding-and-offboarding).
