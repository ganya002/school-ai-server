# GPU & Drivers

> Status: **Not started.** GPU model and VRAM are unknown (M01-009).

| Item | Value | Source |
| --- | --- | --- |
| GPU model / VRAM | TBD | nvidia-smi |
| PCI ID | TBD | lspci |
| Secure Boot | TBD | `mokutil --sb-state` |
| Driver branch | TBD (from `ubuntu-drivers list --gpgpu`) | M08-003 |
| Driver version | TBD | nvidia-smi |
| CUDA version supported by driver | TBD | nvidia-smi |
| CUDA Toolkit needed? | TBD (M08-007) | engine docs |
| Docker + NVIDIA Container Toolkit | Only if Docker is chosen | M08-008/009 |
| Persistence mode | TBD | nvidia-smi |
| Power limit | TBD | nvidia-smi |
| Driver hold policy | TBD | M08-012 |

## Install procedure

Follow the official [Ubuntu NVIDIA driver installation](https://ubuntu.com/server/docs/nvidia-drivers-installation) guide for servers. Do not mix Ubuntu packages with NVIDIA `.run` installers. Container GPU access: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

Record the exact commands used and their output here when done.

## VM path note

With Proxmox, the GPU must be passed through to the VM first ([PCI passthrough](https://pve.proxmox.com/wiki/PCI_Passthrough)); the driver is then installed inside the VM.
