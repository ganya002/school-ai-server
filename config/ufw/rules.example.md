> Not the current plan. Both nodes stay on Windows 11 ([ADR 0001](../../decisions/0001-windows-11-native.md)). Use `config/windows-firewall/rules.example.ps1` instead.

# ufw rules (EXAMPLE, placeholders)

Order matters: allow SSH **before** enabling, and keep console access ready.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
# SSH only from the admin path (VPN interface or range)
sudo ufw allow in on ADMIN_VPN_INTERFACE to any port 22 proto tcp comment 'SSH admins via VPN'
#   or: sudo ufw allow from ADMIN_VPN_RANGE to any port 22 proto tcp
# Web UI over HTTPS for students and admins
sudo ufw allow from STUDENT_NET_RANGE to any port 443 proto tcp comment 'Web UI students'
sudo ufw allow from ADMIN_VPN_RANGE to any port 443 proto tcp comment 'Web UI admins'
sudo ufw enable
sudo ufw status verbose
```

Do **not** open the inference engine port (11434 / 8000 / 8080); it listens on 127.0.0.1 only.

Note: Docker-published ports can bypass ufw rules. If Docker is used, bind published ports to `127.0.0.1` and put a reverse proxy in front, and check Docker's documentation on firewalls.
