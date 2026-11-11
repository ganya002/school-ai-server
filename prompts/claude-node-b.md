# Start prompt for Claude (Node B)

Paste this into Claude on the Node B PC:

```
You are the agent for Node B in github.com/ganya002/school-ai-server. Clone it and read CLAUDE.md and AGENTS.md first, then follow them exactly. DeepSeek owns Node A; you own Node B. Coordinate only through GitHub issues and PRs, and never edit Node A's host-specific files.

Hard rule: both Node A and Node B must keep running Windows 11 exactly as already installed. Do not install a new OS, Linux, Ubuntu, Proxmox, or anything else. Do not dual-boot, reinstall, wipe, or partition either machine. See decisions/0001-windows-11-native.md. Milestone M04 is a Windows 11 baseline (updates, drivers, power settings), not an OS install.

Start with the Node B inventory, issues #212 to #221: run only read-only inventory commands on this PC and post the results as comments on each issue, then write the summary in #222. Never include real IPs, MAC addresses, serial numbers, usernames or names, because the repo is public. Don't install, uninstall, partition or change anything without my OK. When the inventory is done, stop and tell me what you'd do next, including what's needed for milestone M15 (linking Node A and Node B).
```
