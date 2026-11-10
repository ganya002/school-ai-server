# Troubleshooting

> Only problems actually met during the project, with verified fixes (M14-008). Format: **Symptom → Cause → Fix → Issue**.

| Symptom | Likely area | First checks |
| --- | --- | --- |
| Cannot SSH in | SSH / ufw / VPN / fail2ban | Console access; `sudo ufw status`; `sudo fail2ban-client status sshd`; `sudo sshd -t` |
| `nvidia-smi` fails after update | NVIDIA driver / kernel / Secure Boot | `dkms status`; `mokutil --sb-state`; reboot; driver hold policy |
| Model is very slow | CPU offload / context too large | `ollama ps` (or engine log) GPU/CPU split; `nvidia-smi` memory |
| Out of memory errors | Context × parallel too large | Reduce context or parallel slots (see M12-010) |
| Web UI shows no models | Engine down / wrong URL | `systemctl status`; `curl http://127.0.0.1:PORT/...` |
| Students cannot reach web UI | ufw / network / TLS | Port matrix; certificate; IT network rules |

## Recorded problems

| Date | Symptom | Cause | Fix | Issue |
| --- | --- | --- | --- | --- |
| — | *(none yet)* | | | |
