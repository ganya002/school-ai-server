# Start prompt for Claude (Node B) — Phase 2 TTS

Phase 1 inventory on this node is done. Paste the block below into Claude on the Node B PC.

```
You are the agent for Node B (Claude) in github.com/ganya002/school-ai-server. Run git pull, then read CLAUDE.md, AGENTS.md and docs/tts-plan.md and follow them exactly. DeepSeek owns Node A; you own Node B. Never edit Node A's host-specific files.

Phase 1 inventory is done. This is Phase 2: text-to-speech.

Hard rules: both Node A and Node B must keep running Windows 11 exactly as already installed. Do not install a new OS, Linux, Ubuntu, Proxmox, or anything else. Do not dual-boot, reinstall, wipe, or partition either machine. WSL2 or Docker Desktop only with the project owner's OK; they are not the default. See decisions/0001-windows-11-native.md.

Our team does TTS (Norwegian + English). Another group does the LLM. Confirm the lineup in issue #26 if it is not already accepted.

Take the Node B TTS issues, main lineup first, then optional:

Main:
- #240 Install and benchmark VoxCPM2
- #245 Install and benchmark Piper Norwegian (no_NO) on CPU

Optional (label optional, only after the main lineup or if the owner asks):
- #248 Dia / Dia2

For each model: propose the exact install commands in the issue, wait for the project owner's OK (and Node B's human owner in the loop), then install, benchmark (VRAM, time-to-first-audio, RTF, short sample notes) and post the results on the issue. Expose each model as OpenAI-compatible POST /v1/audio/speech on its own 127.0.0.1 port, and document ports in docs/tts-plan.md (placeholder addresses only).

Coordinate with Node A only through GitHub issues and PRs, including the both-node issues #250 (voice picker / router) and #251 (public HTTPS via Tailscale Funnel, needs school IT + teacher OK). Do not buy a domain. The default public path is Tailscale Funnel (outbound only; students need no client). In the repo use only the placeholder https://tts-gateway.example-tailnet.ts.net. Never write a real tailnet, domain or token. Cloudflare named tunnels are only an option if the school later provides a domain; quick tunnels are rejected.

This repository is public. Never include real IPs, names, MAC addresses, serial numbers or tokens. Never git push --force.
```
