# Example configuration

Everything in this folder is an **example with placeholders**. Nothing here has been tested on the real servers yet. Both nodes stay on **Windows 11** ([ADR 0001](../decisions/0001-windows-11-native.md)). Prefer the Windows Firewall and autostart examples below. Older Linux files (`ufw`, `fail2ban`, `unattended-upgrades`, systemd units, sudoers) are leftover references, not the plan.

Copy a file to the server only with Gabby's OK, replace the placeholders, and record the real setting in the matching `docs/` page.

Never put real secrets, keys or uncommittable addresses in these files.

| File | Goes to | Doc |
| --- | --- | --- |
| `windows-firewall/rules.example.ps1` | run (carefully) in an elevated PowerShell, after replacing placeholders | docs/network.md, docs/security-hardening.md |
| `windows/ai-host-autostart.example.md` | Windows service or Task Scheduler | docs/ai-host.md |
| `ssh/10-hardening.conf.example` | Adapt into `C:\ProgramData\ssh\sshd_config` | docs/remote-access.md |
| `open-webui/open-webui.env.example` | env file for Open WebUI | docs/web-ui-and-api.md |
| `ufw/rules.example.md` | *Not the plan* (Linux leftover) | — |
| `fail2ban/jail.local.example` | *Not the plan* (Linux leftover) | — |
| `unattended-upgrades/52-ai-server.example` | *Not the plan* (Linux leftover) | — |
| `sudoers/ai-admins.example` / `ai-operators.example` | Role intent only; use Windows groups | docs/users-and-roles.md |
| `ollama/override.conf.example` / `llama-server/llama-server.service.example` | *Not the plan* (systemd leftovers) | — |
