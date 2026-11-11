# Security Hardening

> Status: **Planned.** Each measure is filled in with real settings and verification output during M05/M06. The host OS is Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)).

| # | Measure | Why | How to verify | Status |
| --- | --- | --- | --- | --- |
| 1 | SSH keys only, no Administrator SSH login, allowed Windows groups only | Stops password guessing and a shared admin login | Inspect `C:\ProgramData\ssh\sshd_config`; `sshd -T` if available | Not started |
| 2 | Windows Defender Firewall: inbound default block; allow only the port matrix | Minimises exposure | `Get-NetFirewallProfile`; `Get-NetFirewallRule` for the allow rules | Not started |
| 3 | SSH only from the admin path | LAN users cannot reach SSH | Test from a student-network device | Not started |
| 4 | No inbound router ports; raw backend APIs and SSH stay private | School routers do not forward ports. Public student access, if approved, is an outbound-only Tailscale Funnel in front of the gateway only | IT confirms no inbound forwarding; Funnel publishes only the gateway | Not started |
| 5 | Anti-lockout for SSH (MaxAuthTries, Windows account lockout; fail2ban is not the plan) | Slows brute-force attempts | Failed-login test from a throwaway key, then confirm a legit key still works | Not started |
| 6 | Windows Update for security patches | Automatic patching | Windows Update history; reboot policy in docs/operations.md | Not started |
| 7 | Reboot policy | Updates take effect without an unexpected outage | docs/operations.md | Not started |
| 8 | Unused services disabled | Smaller attack surface | `Get-NetTCPConnection -State Listen` vs port matrix | Not started |
| 9 | Event Log retention within policy | Audit trail | Event Viewer / `wevtutil gl Security` | Not started |
| 10 | Inference API on 127.0.0.1 only | API cannot be abused from the LAN | `Get-NetTCPConnection -State Listen` | Not started |
| 11 | Web UI: no open sign-up, roles, HTTPS | Only approved users, encrypted logins | M10 tests | Not started |
| 12 | Least-privilege local groups (admins vs operators) | Limits damage from a compromised account | `Get-LocalGroupMember` and a scheduled-task/service ACL check | Not started |
| 13 | Secrets outside Git | Prevents leaks | `.gitignore`, secret-store ADR | Not started |
| 14 | Windows security baseline (Defender on, firewall on); record what was reviewed | Measurable hardening on Windows (Lynis is Linux-oriented and is not the plan) | Defender status; firewall profiles | Not started |
| 15 | Advanced audit policy (optional) | Records privileged actions | Decision M06-010 | Not started |
| 16 | Deployment server / Wazuh (scope TBD) | Central config + security monitoring | M11 | Not started |
| 17 | Per-student API key on every public TTS request | No anonymous use of the gateway | Request without a key is refused | Not started |
| 18 | Rate limits, quotas and request size limits on the gateway | Stops abuse and runaway cost/load | Exceeding the limit is refused | Not started |
| 19 | Abuse / kill switch for a key or the whole public path | Can cut off misuse quickly | Documented switch is tested | Not started |
| 20 | Do not store request text or generated audio | Privacy; only short-lived in-memory processing by default | Config and a policy check | Not started |
| 21 | Tailscale Funnel (default public path) only after IT + teacher approval | Students can reach HTTPS from any network without opening inbound ports | Funnel docs + approval recorded; placeholder URL only in Git | Not started |

## Baseline results

| Date | What was reviewed | Notes |
| --- | --- | --- |
| TBD | | |

## Accepted risks

| Finding | Reason accepted | Accepted by |
| --- | --- | --- |
| TBD | | |

## Public TTS gateway

The planned student path is **Tailscale Funnel** on the gateway node, URL placeholder `https://tts-gateway.example-tailnet.ts.net`. See [tts-plan.md](tts-plan.md) §6–§7 and [client-guide.md](client-guide.md). Do not buy a domain. Do not use Cloudflare quick tunnels. A Cloudflare named tunnel is only an option if the school later provides a domain.

References: [Windows Firewall](https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/) · [OpenSSH on Windows](https://learn.microsoft.com/windows-server/administration/openssh/openssh-overview) · [Windows Update](https://learn.microsoft.com/windows/deployment/update/) · [Microsoft Defender](https://learn.microsoft.com/windows/security/operating-system-security/virus-and-threat-protection/)

Example rules: [`config/windows-firewall/rules.example.ps1`](../config/windows-firewall/rules.example.ps1). Older `config/ufw` and `config/fail2ban` examples are not the plan.
