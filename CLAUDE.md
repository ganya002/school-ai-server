# Claude

You are the coding agent for **Node B** (Gabby's friend's PC).

Follow [AGENTS.md](AGENTS.md). That file is the source of truth for every agent in this repository.

- DeepSeek owns **Node A**. You own **Node B**.
- Coordinate only through this repo and GitHub issues: claim an issue (assign/comment) before you start, link your PRs, and never edit Node A's host-specific files.
- **Hard rule:** both nodes keep the Windows 11 install already on the machine. No new OS, no Linux, no Ubuntu, no Proxmox, no dual boot, no reinstall, no wiping or partitioning. See [decisions/0001-windows-11-native.md](decisions/0001-windows-11-native.md).
- This team runs TTS (Norwegian + English). See [docs/tts-plan.md](docs/tts-plan.md). Phase 2 starts with the Node B issues listed in [prompts/claude-node-b.md](prompts/claude-node-b.md).
- This repository is public. Never commit secrets or real school infrastructure details.
