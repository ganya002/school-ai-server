# Remote Access

> Status: **Planned.** The access method is decided in M03-010. **The server is never exposed to the public internet.** Both nodes use **OpenSSH Server on Windows 11** ([ADR 0001](../decisions/0001-windows-11-native.md)).

## 1. Requirements

| Scenario | Needed? | Method |
| --- | --- | --- |
| Admins on the school network | Yes | SSH over the admin path |
| Admins off-site | TBD (M01-018) | School VPN / Tailscale / WireGuard (TBD) |
| Students on the school network | Yes (web UI only) | HTTPS |
| Students off-site | TBD (M01-018) | TBD, only through an approved private path |

## 2. SSH policy

- Install and enable [OpenSSH Server on Windows](https://learn.microsoft.com/windows-server/administration/openssh/openssh-overview) (optional feature). Node B already had it running at inventory time; confirm it stays enabled after reboots.
- Keys only (`PasswordAuthentication no`, `KbdInteractiveAuthentication no`).
- Do not allow SSH as `Administrator` (`PermitRootLogin no`, or the Windows equivalent).
- Only the approved admin and operator accounts or Windows groups (`AllowUsers` / `AllowGroups`).
- Personal ed25519 keys with passphrases; private keys never leave the owner's device.
- Slow down brute-force attempts with `MaxAuthTries` and Windows account lockout (fail2ban is not the plan).

Config lives in `C:\ProgramData\ssh\sshd_config`. A Linux-style drop-in example remains at [`config/ssh/10-hardening.conf.example`](../config/ssh/10-hardening.conf.example) for the *settings* to apply; adapt paths and group names to Windows. Always validate the config and keep a second session or a physical console available before restarting `sshd`.

## 3. Private access path (M03-010, M05-006)

| Option | Notes |
| --- | --- |
| School VPN | Preferred if available; IT manages it |
| Tailscale | Needs IT approval (external coordination service). Restrict with ACLs ([docs](https://tailscale.com/kb/1018/acls)) |
| WireGuard | Self-hosted; needs a reachable endpoint, which may require IT changes |
| LAN only | Simplest; no off-site access |

Chosen: TBD.

## 4. Emergency / console access (M05-009)

There is no Proxmox console. Use a physical keyboard and monitor, or BMC/IPMI only if the inventory shows one.

| Path | Who | Tested |
| --- | --- | --- |
| Physical keyboard/monitor | TBD | TBD |
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

See [users-and-roles.md](users-and-roles.md#onboarding-and-offboarding). On Windows, admin keys often go in `C:\ProgramData\ssh\administrators_authorized_keys` or the user's `.ssh\authorized_keys`. Record the chosen method here when it is set up. Never commit keys.
