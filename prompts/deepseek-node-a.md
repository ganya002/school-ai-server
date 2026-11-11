# Start prompt for DeepSeek (Node A) — Phase 2 TTS

Phase 1 inventory on this node is done. Paste the block below into DeepSeek on the Node A PC.

```
You are the agent for Node A (DeepSeek) in github.com/ganya002/school-ai-server. Run git pull, then read AGENTS.md and docs/tts-plan.md and follow them exactly.

Phase 1 inventory is done. This is Phase 2: text-to-speech.

Hard rules: both Node A and Node B must keep running Windows 11 exactly as already installed. Do not install a new OS, Linux, Ubuntu, Proxmox, or anything else. Do not dual-boot, reinstall, wipe, or partition either machine. WSL2 or Docker Desktop only with my OK; they are not the default. See decisions/0001-windows-11-native.md.

Our team does TTS (Norwegian + English). Another group does the LLM. Confirm the lineup in issue #26 if it is not already accepted.

Take the Node A TTS issues, main lineup first, then optional:

Main:
- #241 Install and benchmark Qwen3-TTS 12Hz 1.7B
- #242 Install and benchmark Phonon 31M
- #243 Install and benchmark Kokoro-82M via Kokoro-FastAPI
- #244 Install and benchmark Piper Norwegian (no_NO) on CPU

Optional (label optional, only after the main lineup or if I ask):
- #246 Ming-3.0-tts-0.5B
- #247 Orpheus 3B (Llama-based weight terms; not for the public service until approved)
- #249 Sesame CSM-1B

Before any PyTorch model on this PC (RTX 5070 Ti, Blackwell), install a cu128+ build and verify that sm_120 is in torch.cuda.get_arch_list(). The 16 GB figure is the discrete GPU only; iGPU memory does not add to it.

For each model: propose the exact install commands in the issue, wait for my OK, then install, benchmark (VRAM, time-to-first-audio, RTF, short sample notes) and post the results on the issue. Expose each model as OpenAI-compatible POST /v1/audio/speech on its own 127.0.0.1 port, and document ports in docs/tts-plan.md (placeholder addresses only).

Coordinate with Node B only through GitHub issues and PRs, including the both-node issues #250 (voice picker / router) and #251 (public HTTPS via Tailscale Funnel, needs school IT + teacher OK). Do not buy a domain. The default public path is Tailscale Funnel (outbound only; students need no client). In the repo use only the placeholder https://tts-gateway.example-tailnet.ts.net. Never write a real tailnet, domain or token. Cloudflare named tunnels are only an option if the school later provides a domain; quick tunnels are rejected.

This repository is public. Never include real IPs, names, MAC addresses, serial numbers or tokens. Never git push --force.
```
