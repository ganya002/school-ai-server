# Operations

> Status: **Draft.** Completed in M14-006.

## Project context

| Item | Value |
| --- | --- |
| Assignment | Prosjekt 09 — AI-server setup (Drift og Utvikling) |
| Assessment form | TBD (M01-002) |
| Allowed operating hours | TBD (M01-016) |
| Reboot policy | TBD (M06-007) |

## Daily checks

```bash
systemctl --failed
systemctl status <engine-service> <webui-service>
nvidia-smi
df -h
sudo ufw status
sudo fail2ban-client status sshd
```

## Start / stop / restart

TBD (service names per ADR).

## Updates

| Component | How | Who | When |
| --- | --- | --- | --- |
| OS security updates | unattended-upgrades | automatic | daily |
| OS other updates | `apt full-upgrade` | ai-admins | TBD |
| NVIDIA driver | per hold policy | ai-admins | maintenance window |
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
