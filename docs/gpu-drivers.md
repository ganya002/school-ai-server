# GPU & Drivers

> Status: **Not started.** GPU model and VRAM are unknown until the inventory is complete (M01-009). Drivers are installed on the existing Windows 11 system ([ADR 0001](../decisions/0001-windows-11-native.md)).

| Item | Value | Source |
| --- | --- | --- |
| GPU model / VRAM | TBD | nvidia-smi |
| PCI ID | TBD | Device Manager / `Get-PnpDevice` |
| Secure Boot | TBD | firmware / `Confirm-SecureBootUEFI` |
| Driver branch | TBD (NVIDIA Game Ready or Studio, from the official Windows driver) | M08-003 |
| Driver version | TBD | nvidia-smi |
| CUDA version supported by driver | TBD | nvidia-smi |
| CUDA Toolkit needed? | TBD (M08-007) | engine docs |
| Docker + NVIDIA Container Toolkit | Only if Docker / WSL2 is later approved by Gabby | M08-008/009 |
| Persistence mode | TBD (if applicable on Windows) | nvidia-smi |
| Power limit | TBD | nvidia-smi |
| Driver hold / update policy | TBD | M08-012 |

## Install procedure

Install the official [NVIDIA Windows driver](https://www.nvidia.com/Download/index.aspx) that matches the inventoried GPU. Prefer the installer from NVIDIA, not a random third-party package. Do not install a Linux driver, and do not pass the GPU into a VM: both nodes stay on native Windows 11.

Record the exact installer version and `nvidia-smi` output here when done (no serials).

If Docker Desktop or WSL2 is later approved, follow NVIDIA's Windows/WSL GPU guidance at that time. It is not the default.
