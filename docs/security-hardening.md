# Security Hardening

> Status: **Planned.** Each measure is filled in with real settings and verification output during M05/M06.

| # | Measure | Why | How to verify | Status |
| --- | --- | --- | --- | --- |
| 1 | SSH keys only, no root login, AllowGroups | Stops password guessing and shared root | `sudo sshd -T \| grep -Ei 'passwordauth\|permitroot\|allowgroups'` | Not started |
| 2 | ufw default deny incoming; allow only the port matrix | Minimises exposure | `sudo ufw status verbose` | Not started |
| 3 | SSH only from the admin path | LAN users cannot reach SSH | Test from a student-network device | Not started |
| 4 | No internet exposure | Keeps the uncensored model and admin access internal | IT confirms no forwarding (M06-003) | Not started |
| 5 | fail2ban sshd jail | Bans brute-force attempts | `sudo fail2ban-client status sshd` | Not started |
| 6 | unattended-upgrades (security) | Automatic patching | `sudo unattended-upgrade --dry-run --debug` | Not started |
| 7 | Reboot policy | Kernel patches take effect | docs/operations.md | Not started |
| 8 | Unused services disabled | Smaller attack surface | `sudo ss -tulpn` vs port matrix | Not started |
| 9 | Persistent journald with retention | Audit trail within policy | `journalctl --list-boots` | Not started |
| 10 | Inference API on 127.0.0.1 only | API cannot be abused from the LAN | `ss -tlpn` | Not started |
| 11 | Web UI: no open sign-up, roles, HTTPS | Only approved users, encrypted logins | M10 tests | Not started |
| 12 | Sudo least privilege (operators limited) | Limits damage from a compromised account | `sudo -l -U <user>` | Not started |
| 13 | Secrets outside Git | Prevents leaks | `.gitignore`, secret-store ADR | Not started |
| 14 | Lynis baseline + fixes | Measurable hardening | Hardening index before/after | Not started |
| 15 | auditd (optional) | Records privileged actions | Decision M06-010 | Not started |
| 16 | Deployment server / Wazuh (scope TBD) | Central config + security monitoring | M11 | Not started |

## Lynis results

| Date | Lynis version | Hardening index | Warnings | Notes |
| --- | --- | --- | --- | --- |
| TBD | | | | |

## Accepted risks

| Finding | Reason accepted | Accepted by |
| --- | --- | --- |
| TBD | | |

References: [Ubuntu firewalls](https://ubuntu.com/server/docs/how-to/security/firewalls) · [OpenSSH server](https://ubuntu.com/server/docs/openssh-server) · [sshd_config](https://manpages.ubuntu.com/manpages/noble/man5/sshd_config.5.html) · [fail2ban](https://github.com/fail2ban/fail2ban) · [Automatic updates](https://documentation.ubuntu.com/server/how-to/software/automatic-updates/) · [Lynis](https://cisofy.com/lynis/)
