# Windows Defender Firewall rules (EXAMPLE, placeholders only)
# Do not run this on a live PC without Gabby's OK (and Node B's owner for Node B).
# Replace ADMIN_VPN_RANGE, STUDENT_NET_RANGE, PEER_NODE_IP, and ports first.
# Reference: https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/

# Show current profiles (expected: inbound blocked for the profiles you use)
Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction, DefaultOutboundAction

# SSH: admins only (use the school VPN/admin range, never "any")
New-NetFirewallRule -DisplayName "AI-SSH-Admins" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22 -RemoteAddress ADMIN_VPN_RANGE -Profile Any

# Web UI HTTPS: students + admins
New-NetFirewallRule -DisplayName "AI-WebUI-HTTPS" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 443 -RemoteAddress STUDENT_NET_RANGE,ADMIN_VPN_RANGE -Profile Any

# Interconnect: only the peer node, only the agreed inference port (if the API is not localhost-only)
# New-NetFirewallRule -DisplayName "AI-Interconnect-Inference" -Direction Inbound -Action Allow -Protocol TCP -LocalPort PORT -RemoteAddress PEER_NODE_IP -Profile Any

Get-NetFirewallRule -DisplayName "AI-*" | Format-Table DisplayName, Enabled, Direction, Action
