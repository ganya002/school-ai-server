# Windows 11 baseline

> Status: **Decided.** Both nodes keep the Windows 11 install already on the machine. See [ADR 0001](../decisions/0001-windows-11-native.md). This page is a baseline checklist, not an operating-system install guide.

## Hard rule

Do **not** install a new OS, Linux, Ubuntu, Proxmox, or any other system. Do not dual-boot, reinstall, wipe, or partition either machine.

## 1. Permission and conditions (M01-005)

Permission is to *use* the existing Windows 11 installs and to install AI software and drivers. It is not permission to replace the OS.

| Item | Value |
| --- | --- |
| Teacher permission | TBD |
| IT permission | TBD |
| May the machine be wiped or reinstalled? | **No** (ADR 0001) |
| IT conditions (maintenance windows, who may be a local admin) | TBD |

## 2. Current operating system

| Item | Node A | Node B | Source |
| --- | --- | --- | --- |
| OS | Windows 11, edition/build TBD | Windows 11 Home 25H2 (build 26200) | Inventory; ADR 0001 |
| Firmware | TBD | UEFI, Secure Boot off | Inventory |
| Disks | Existing layout only; do not repartition | Existing Windows volume; do not repartition | Inventory |

Record edition, build and feature updates here when the baseline is done. Do not change edition or reinstall to "get a server OS".

## 3. Baseline steps (M04)

Do these on the live Windows 11 system. Applying changes on a real PC needs Gabby's OK (and Node B's owner for Node B).

| Step | What to do | How to check (PowerShell) |
| --- | --- | --- |
| Admin account | A named personal admin account exists; no shared "admin" login | `Get-LocalGroupMember Administrators` (usernames only in the repo) |
| Hostname | Set or confirm the approved name; use a placeholder in Git | `hostname` |
| Stable address | Static IP or a DHCP reservation from IT | `Get-NetIPConfiguration` after a reboot (placeholders in Git) |
| Time | Time zone `Europe/Oslo`; Windows Time service syncing | `Get-TimeZone`; `w32tm /query /status` |
| Updates | Install all current Windows updates, then reboot if required | Settings → Windows Update, or `Get-HotFix` |
| GPU driver | Official [NVIDIA Windows driver](https://www.nvidia.com/Download/index.aspx) for the inventoried GPU (M08) | `nvidia-smi` |
| Power plan | While plugged in: no sleep, no hibernate, so the AI host stays reachable | `powercfg /query`; `powercfg /a` |
| OpenSSH Server | Optional Windows feature, enabled (M05) | `Get-Service sshd` |
| Baseline backup | Windows backup or a documented copy of config; not a Proxmox snapshot | Date recorded in [backup.md](backup.md) |

Suggested power-plan commands (do not run without OK):

```powershell
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /hibernate off
powercfg /change monitor-timeout-ac 0
```

## 4. Disks and model path (no repartition)

Keep the existing volumes. Choose a folder on an existing drive for models, for example `C:\AI\models` (exact path TBD in M03). Record free space in the inventory. Do not shrink, wipe, or reformat partitions.

## 5. BIOS / UEFI (record only unless a change is approved)

| Setting | Before | After | Approved by |
| --- | --- | --- | --- |
| Secure Boot | TBD per node | | |
| Boot order | TBD | | |
| Power on after power loss | TBD | | |

Do not change firmware settings without the owner and, if required, IT.

## 6. What this page is not

There is no installer ISO, no bootable USB, no Proxmox VM, and no GPU passthrough into a guest. Those paths were dropped by ADR 0001.
