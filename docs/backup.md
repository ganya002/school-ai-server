# Backup & Restore

> Status: **Planned.** Scope and location are decided in M14-001. Both nodes stay on Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)); there is no Proxmox snapshot path.

| What | Included | Where | How often | Retention |
| --- | --- | --- | --- | --- |
| Open WebUI data (users, settings, chats per policy) | Yes | TBD (IT-approved) | TBD | Per retention ADR |
| Host config (OpenSSH, firewall export, engine/web UI config, scheduled tasks) | Yes | TBD | TBD | TBD |
| This repository (docs, ADRs) | GitHub | GitHub | on push | — |
| Model weights | **No** (re-downloadable; record exact file + checksum instead) | — | — | — |
| Secrets | Only in the secret store | — | — | — |
| Windows baseline backup (after M04) | TBD (Windows Backup, a system image, or a documented config copy) | TBD | after the baseline, then TBD | TBD |

Open WebUI backup guidance: [official tutorial](https://docs.openwebui.com/tutorials/maintenance/backups).

## Restore procedure

TBD (M14-004). Always test restore on a test instance, not over production. Do not recover by reinstalling or partitioning Windows.

## Restore tests

| Date | What | Result | Time needed |
| --- | --- | --- | --- |
| TBD | | | |
