# 0001: Both nodes stay on Windows 11

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-11-11 |
| Person responsible | Gabby |
| Approved by | Gabby (project owner), 2026-11-11 |
| Related issues | #39, #44, M04 issues #54–#68 and #223, #5 |

## Context

Both school PCs that will be Node A and Node B already run Windows 11 (Node B is recorded as Windows 11 Home 25H2 in the inventory; Node A's exact edition is in the inventory work). The assignment text allows installing an operating system, and early plans assumed Ubuntu Server LTS, either bare metal or as a Proxmox VM with GPU passthrough.

On 2026-11-11 Gabby set a hard project rule: **both nodes must keep running Windows 11 exactly as already installed.** A new OS, a Linux or Ubuntu install, Proxmox, a dual boot, a reinstall, or any wipe or partition of either machine is out of scope.

Teacher and school IT approval is still required to *use* the machines and to install AI software and drivers. That approval is not permission to replace the operating system.

## Available options

### Option A: Keep the installed Windows 11 on both nodes

Leave the existing Windows 11 installs in place. Treat milestone M04 as a Windows 11 baseline (updates, drivers, power settings, hostname, time, backup), not an OS install. Run the inference backend and related services natively on Windows.

- **Advantages:**
  - Honours the project owner's hard rule and preserves existing data and apps.
  - Avoids wipe/reinstall risk, dual-boot complexity, and GPU passthrough work.
  - NVIDIA drivers and several inference engines already have official Windows support.
- **Disadvantages:**
  - Some earlier docs and issues assumed Ubuntu, ufw, systemd and Proxmox, and must be rewritten.
  - A few Linux-first tools (for example vLLM, Lynis, unattended-upgrades, fail2ban) are a poor or incomplete fit and need Windows equivalents.
  - Windows 11 Home (Node B) lacks some Pro-only features; the plan must not assume them.

### Option B: Replace Windows with Ubuntu Server (bare metal)

Wipe or dual-boot and install Ubuntu Server LTS on each PC.

- **Advantages:**
  - Matches the original draft architecture (ufw, systemd, apt).
- **Disadvantages:**
  - Contradicts the owner's hard rule. Destroys or relocates the existing OS and data.

### Option C: Install Proxmox and run Ubuntu in a VM with GPU passthrough

- **Advantages:**
  - Snapshots and a hypervisor console.
- **Disadvantages:**
  - Contradicts the owner's hard rule. Needs a new OS on the metal, IOMMU setup, and GPU passthrough.

## Chosen solution

**Option A.** Both Node A and Node B stay on the Windows 11 install already on the machine.

- No new OS, no Linux, no Ubuntu, no Proxmox, no dual boot, no reinstall, no wiping, and no partitioning.
- M04 is "prepare the Windows 11 baseline": Windows Update, official NVIDIA drivers on Windows, timezone `Europe/Oslo`, a stable address, a personal admin account, a power plan that does not sleep, OpenSSH Server for Windows, and a baseline backup. It is not an install guide.
- The inference backend must run natively on Windows (for example [Ollama for Windows](https://docs.ollama.com/windows) or llama.cpp's Windows server build). The model remains **TBD**.
- Open WebUI or a similar UI should use a Windows-friendly method (for example a native Python install). **WSL2 or Docker Desktop is optional only, and needs Gabby's OK; it is not the default.**
- Host firewall: **Windows Defender Firewall**, not ufw.
- Remote access: **OpenSSH Server on Windows**, key-only.
- Autostart: **Windows services or Task Scheduler**, not systemd.
- Power: disable sleep/hibernate while plugged in so the AI host stays reachable.

## Reason for the decision

Gabby, as project owner, required that the existing Windows 11 installs be kept. Option B and option C are incompatible with that rule. Option A still meets the assignment: a reachable AI host on the school LAN, remote access over SSH, and no public internet exposure, without replacing the operating system.

## Consequences

- Docs, start prompts, agent rules and GitHub issues that assumed a Linux or Proxmox install are updated to this plan. Issues that exist only to download an ISO, write a USB installer, create a Proxmox VM or install Ubuntu are closed as **not planned** (never deleted). Remaining M04 issues are rewritten as Windows 11 baseline work.
- Earlier expected decisions "Physical install vs Proxmox VM" and "OS version" are settled by this ADR: physical Windows 11 as already installed. The exact Windows 11 edition and build per node stay in the inventory.
- Engine research should prefer software with a real Windows path. vLLM is typically Linux/Docker and is a weak default unless a later, approved exception is made.
- Linux-oriented example configs under `config/ufw`, `config/unattended-upgrades` and systemd unit examples are not the plan. Windows Firewall and service examples replace them for implementation work.

## References

- [docs/os-installation.md](../docs/os-installation.md) — Windows 11 baseline
- [docs/architecture.md](../docs/architecture.md)
- [docs/ai-host.md](../docs/ai-host.md)
- [docs/two-node-cluster.md](../docs/two-node-cluster.md)
- [AGENTS.md](../AGENTS.md) hard rules
- https://docs.ollama.com/windows
- https://learn.microsoft.com/windows-server/administration/openssh/openssh-overview
- https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/
