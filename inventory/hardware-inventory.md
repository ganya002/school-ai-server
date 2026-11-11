# Hardware Inventory — School AI Server

> Two machines: **Node A** (Gabby / DeepSeek) and **Node B** (Gabby's friend / Claude). Fill in with school IT. Only record details IT allows in this repository (M01-006); **never** passwords. Unknown: `TBD`.

Helper (read-only, run only on an already running Linux system with IT's permission): [`scripts/linux/collect-hardware-inventory.sh`](../scripts/linux/collect-hardware-inventory.sh).

## Node A

| Item | Value | Source / date |
| --- | --- | --- |
| Machine (asset tag / nickname) | TBD | |
| Location (server room / classroom) | TBD | |
| Whole machine or VM for the team | TBD | |
| Currently running (empty / OS / Proxmox VE version) | TBD | |
| Data that must be preserved | TBD | |
| CPU model | TBD | |
| Cores / threads | TBD | |
| Installed RAM | TBD | |
| Free DIMM slots / max RAM | TBD | |
| GPU model(s) | TBD | |
| VRAM per GPU | TBD | |
| GPU PCI ID | TBD | |
| PSU wattage / GPU recommended PSU | TBD | |
| IOMMU (VT-d / AMD-Vi) support | TBD | |
| Disk 1 (type, size) | TBD | |
| Disk 2 (type, size) | TBD | |
| NICs and link speed | TBD | |
| Cooling / UPS | TBD | |
| Allowed operating hours | TBD | |
| BMC / IPMI present | TBD | |

## Node B

| Item | Value | Source / date |
| --- | --- | --- |
| Machine (asset tag / nickname) | Komplett desktop, ASUS TUF GAMING B760-PLUS WIFI D4 (hostname not recorded: `AI_NODE_B_HOSTNAME`) | CIM, 2026-11-11 (#222) |
| Location (server room / classroom) | TBD (owner to confirm) | #221 |
| Whole machine or VM for the team | Whole machine (bare metal) | #217, #218 |
| Currently running (empty / OS / Proxmox VE version) | Windows 11 Home 25H2 (build 26200), UEFI, Secure Boot off. No Proxmox, WSL, Docker or Ollama. OpenSSH server running. | CIM, 2026-11-11 (#217) |
| Data that must be preserved | TBD (owner to decide): one user profile (~7.5 GB) and installed apps (~33 GB) | #215, #217 |
| CPU model | Intel Core i5-13600KF (no iGPU) | CIM, 2026-11-11 (#212) |
| Cores / threads | 14 (6P + 8E) / 20 | CIM, 2026-11-11 (#212) |
| Installed RAM | 64 GB DDR4-3200 (2 × 32 GB) | CIM, 2026-11-11 (#213) |
| Free DIMM slots / max RAM | 2 of 4 free / 128 GB | CIM, 2026-11-11 (#213) |
| GPU model(s) | 1 × NVIDIA GeForce RTX 4070 Ti | nvidia-smi, 2026-11-11 (#214) |
| VRAM per GPU | 12 GB (12282 MiB) | nvidia-smi, 2026-11-11 (#214) |
| GPU PCI ID | 10de:2782 (PCIe Gen 4 x16) | CIM, 2026-11-11 (#214) |
| PSU wattage / GPU recommended PSU | TBD (not readable from software) / NVIDIA recommends 700 W; GPU power limit 285 W (max 314 W) | nvidia-smi, 2026-11-11 (#220) |
| IOMMU (VT-d / AMD-Vi) support | Yes: VT-x on, VT-d available (Windows reports DMA protection). BIOS screen not checked. | Win32_DeviceGuard, 2026-11-11 (#219) |
| Disk 1 (type, size) | NVMe SSD, Kingston NV2 2 TB; ~1738 GB free; holds Windows | Get-PhysicalDisk, 2026-11-11 (#215) |
| Disk 2 (type, size) | None | Get-PhysicalDisk, 2026-11-11 (#215) |
| NICs and link speed | Realtek 2.5 GbE (linked at **100 Mbps only**, check cable/port); Intel Wi-Fi 6 AX201 | Get-NetAdapter, 2026-11-11 (#216) |
| Cooling / UPS | TBD (owner to confirm); no UPS reported to Windows | #221 |
| Allowed operating hours | TBD (owner / IT); sleep is currently enabled | #221 |
| BMC / IPMI present | No (consumer board) | Board model, 2026-11-11 |
