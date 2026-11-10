#!/usr/bin/env bash
# Read-only hardware facts for inventory/hardware-inventory.md.
# Run only on an already running Linux system and only with IT's permission.
# It changes nothing. Review the output before sharing: remove anything IT does not allow in the repo.
set -u
section() { printf '\n## %s\n' "$1"; }
have() { command -v "$1" >/dev/null 2>&1; }

section "Date"; date -Iseconds
section "OS"; (. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME") || uname -a
section "Kernel"; uname -r
section "Virtualisation"; if have systemd-detect-virt; then systemd-detect-virt || true; else echo "unknown"; fi
section "CPU"; if have lscpu; then lscpu | grep -E '^(Model name|Socket\(s\)|Core\(s\) per socket|Thread\(s\) per core|CPU\(s\)):' ; fi
section "RAM"; free -h | sed -n '1,2p'
section "GPU (PCI)"; if have lspci; then lspci -nn | grep -Ei 'vga|3d|display' || echo "none found"; else echo "lspci not installed"; fi
section "GPU (nvidia-smi)"
if have nvidia-smi; then
  nvidia-smi --query-gpu=name,memory.total,driver_version,power.limit --format=csv
else
  echo "nvidia-smi not available (driver not installed yet?)"
fi
section "Disks"; lsblk -d -o NAME,SIZE,ROTA,TYPE,MODEL 2>/dev/null | grep -v '^loop' || true
section "Filesystems"; df -h -x tmpfs -x devtmpfs -x squashfs 2>/dev/null || true
section "Network interfaces"
for i in /sys/class/net/*; do
  n=$(basename "$i"); [ "$n" = lo ] && continue
  printf '%s state=%s speed=%s\n' "$n" "$(cat "$i/operstate" 2>/dev/null)" "$(cat "$i/speed" 2>/dev/null || echo '?')"
done
section "IOMMU"
if dmesg 2>/dev/null | grep -qiE 'DMAR|IOMMU|AMD-Vi'; then echo "IOMMU messages present in dmesg"; else echo "no IOMMU messages visible (may need sudo, or IOMMU is off)"; fi
section "Secure Boot"; if have mokutil; then mokutil --sb-state 2>/dev/null || true; else echo "mokutil not installed"; fi
