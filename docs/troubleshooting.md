# Troubleshooting

> Only problems actually met during the project, with verified fixes (M14-008). Format: **Symptom → Cause → Fix → Issue**. Host OS is Windows 11 ([ADR 0001](../decisions/0001-windows-11-native.md)).

| Symptom | Likely area | First checks |
| --- | --- | --- |
| Cannot SSH in | OpenSSH / Windows Firewall / VPN / account lockout | Physical console; `Get-Service sshd`; `Get-NetFirewallRule`; Event Log for sshd |
| `nvidia-smi` fails after update | NVIDIA Windows driver / Secure Boot | Device Manager; a reboot; driver version vs the hold policy |
| Model is very slow | CPU offload / context too large | `ollama ps` (or engine log) GPU/CPU split; `nvidia-smi` memory |
| Out of memory errors | Context × parallel too large | Reduce context or parallel slots (see M12-010) |
| Web UI shows no models | Engine down / wrong URL | `Get-Service`; `curl.exe http://127.0.0.1:PORT/...` |
| Students cannot reach web UI | Windows Firewall / network / TLS | Port matrix; certificate; IT network rules |
| Node is unreachable after idle | Sleep / hibernate | Power plan in [os-installation.md](os-installation.md); `powercfg /a` |

## Recorded problems

| Date | Symptom | Cause | Fix | Issue |
| --- | --- | --- | --- | --- |
| — | *(none yet)* | | | |
