# OS Installation

> Status: **Not started.** Values are TBD until M01/M03 are done.

## 1. Permission and conditions (M01-005)

| Item | Value |
| --- | --- |
| Teacher permission | TBD |
| IT permission | TBD |
| May the machine be wiped? | TBD |
| IT conditions (maintenance windows, root access) | TBD |

## 2. Decisions

| Item | Value | Source |
| --- | --- | --- |
| Physical or VM | TBD | ADR |
| OS / version | Ubuntu Server LTS, version TBD ([release cycle](https://ubuntu.com/about/release-cycle)) | ADR |
| ISO filename + SHA256 | TBD | M04-001 |
| Installer media | Proxmox ISO storage / USB | M04-002 / M04-005 |

## 3. Disk layout (M03-017)

| Mount | Size | Purpose |
| --- | --- | --- |
| `/` | TBD | OS |
| `/srv/ai/models` (placeholder) | TBD (≥ primary + fallback model) | Model files |
| `/var/lib/…` (web UI data) | TBD | Web UI data |
| Swap | TBD | |

## 4. VM settings (VM path only)

| Setting | Value |
| --- | --- |
| VM ID / name | TBD |
| vCPU / RAM | TBD |
| Disk(s) | TBD |
| Machine type / BIOS | TBD (q35 + OVMF is typical for PCI passthrough, see [Proxmox PCI passthrough](https://pve.proxmox.com/wiki/PCI_Passthrough)) |
| GPU passthrough | TBD |
| Host changes made by/with IT | TBD |

## 5. BIOS settings (physical path only)

| Setting | Before | After | Approved by |
| --- | --- | --- | --- |
| Secure Boot | TBD | | |
| Boot order | TBD | | |
| Power on after power loss | TBD | | |

## 6. Post-install steps

1. Personal admin account created (M04-008).
2. Hostname set (M04-009).
3. Stable IP (M04-010).
4. Timezone `Europe/Oslo` + NTP (M04-011).
5. Full update (M04-012).
6. Baseline snapshot / backup (M04-014).

Record actual dates and versions here when done.
