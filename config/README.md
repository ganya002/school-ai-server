# Example configuration

Everything in this folder is an **example with placeholders**. Nothing here has been tested on the real server yet (the sudoers and sshd examples were only syntax-checked with `visudo -c` and `sshd -t`). Copy a file to the server, replace the placeholders, validate it (e.g. `sshd -t`, `visudo -c`), and record the real setting in the matching `docs/` page.

Never put real secrets, keys or uncommittable addresses in these files.

| File | Goes to | Doc |
| --- | --- | --- |
| `ssh/10-hardening.conf.example` | `/etc/ssh/sshd_config.d/10-hardening.conf` | docs/remote-access.md |
| `ufw/rules.example.md` | commands | docs/network.md |
| `fail2ban/jail.local.example` | `/etc/fail2ban/jail.local` | docs/security-hardening.md |
| `unattended-upgrades/52-ai-server.example` | `/etc/apt/apt.conf.d/52-ai-server` | docs/security-hardening.md |
| `sudoers/ai-admins.example` | `/etc/sudoers.d/ai-admins` (edit with `visudo -f`) | docs/users-and-roles.md |
| `sudoers/ai-operators.example` | `/etc/sudoers.d/ai-operators` | docs/users-and-roles.md |
| `ollama/override.conf.example` | `/etc/systemd/system/ollama.service.d/override.conf` | docs/ai-host.md |
| `llama-server/llama-server.service.example` | `/etc/systemd/system/llama-server.service` | docs/ai-host.md |
| `open-webui/open-webui.env.example` | env file for Open WebUI | docs/web-ui-and-api.md |
