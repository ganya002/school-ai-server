# Operations

> Status: **Draft.** Completed in M14-006. Host OS is Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)).

## Project context

| Item | Value |
| --- | --- |
| Assignment | Prosjekt 09 — AI-server setup (Drift og Utvikling) |
| Assessment form | TBD (M01-002) |
| Allowed operating hours | TBD (M01-016) |
| Reboot policy | TBD (M06-007) |
| Power plan | No sleep / hibernate on AC power (see [os-installation.md](os-installation.md)) |

## Daily checks

```powershell
Get-Service <engine-service>, <webui-service>, sshd
nvidia-smi
Get-PSDrive -PSProvider FileSystem
Get-NetFirewallProfile
Get-WinEvent -LogName Security -MaxEvents 20   # or a documented log query
```

## Start / stop / restart

TBD (service or Task Scheduler names per ADR). Prefer `Restart-Service` / Task Scheduler, not systemd.

## Updates

| Component | How | Who | When |
| --- | --- | --- | --- |
| Windows security updates | Windows Update | automatic, within the reboot policy | TBD |
| Other Windows updates | Windows Update, manual approve if needed | ai-admins | TBD |
| NVIDIA driver | per hold / update policy | ai-admins | maintenance window |
| Inference engine | TBD | ai-admins | TBD |
| Web UI | TBD | ai-admins | TBD |
| Model | Model update procedure + approval | per approval rule (M02-014) | when approved |

## Users

- New student accounts: TBD (method per ADR; credential handout method TBD, never in public chats).
- End of school year: disable/delete student accounts and chats per retention policy (M02-010).

## Handling misuse reports

See [acceptable-use-policy.md §7](acceptable-use-policy.md#7-reporting-misuse-m02-013).

## Model updates and approval

TBD (M14-007). Every new model needs: licence check, approval per the approval rule, VRAM fit check, download from the official repository, checksum, test, rollback plan.

## Monitoring

TBD (M14-005).
