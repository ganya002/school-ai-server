# Backup & Restore

> Status: **Planned.** Scope and location are decided in M14-001.

| What | Included | Where | How often | Retention |
| --- | --- | --- | --- | --- |
| Open WebUI data (users, settings, chats per policy) | Yes | TBD (IT-approved) | TBD | Per retention ADR |
| `/etc` configs (ssh, ufw, fail2ban, sudoers, engine/web UI drop-ins) | Yes | TBD | TBD | TBD |
| This repository (docs, ADRs) | GitHub | GitHub | on push | — |
| Model weights | **No** (re-downloadable; record exact file + checksum instead) | — | — | — |
| Secrets | Only in the secret store | — | — | — |
| Baseline OS snapshot (VM path) | TBD | Proxmox | after install | TBD |

Open WebUI backup guidance: [official tutorial](https://docs.openwebui.com/tutorials/maintenance/backups).

## Restore procedure

TBD (M14-004). Always test restore on a test instance, not over production.

## Restore tests

| Date | What | Result | Time needed |
| --- | --- | --- | --- |
| TBD | | | |
