# Agent guide

This file is the source of truth for every coding agent working in this repository (DeepSeek, Claude, Cursor, and others). Humans on the team should read it too.

## Project goal

Build a **school AI server** for IM students at a Norwegian upper-secondary school (VGS), as Prosjekt 09 in *Drift og Utvikling*.

- Local only: a web UI and, for permitted users, an API.
- Nothing is exposed to the public internet.
- The plan uses **two PCs** on the school LAN. See [docs/two-node-cluster.md](docs/two-node-cluster.md).
- **Model: TBD** (see [docs/model-selection.md](docs/model-selection.md)). Do not pick a model on your own and do not plan an abliterated or uncensored model.

Work follows the [GitHub project board](https://github.com/users/ganya002/projects/5).

## Two nodes and who owns them

| Node | Human owner | Agent | Owns |
| --- | --- | --- | --- |
| **Node A** | Gabby | **DeepSeek** | Inventory, OS, hardening and AI host on PC A |
| **Node B** | Gabby's friend | **Claude** | The same work on PC B |
| **Both** | Either, after claiming the issue | Either | Shared docs, policy, example configs, and the interconnect (M15) |

If you are DeepSeek, you own Node A. If you are Claude, you own Node B. If you are unsure, say so in the issue and do not touch host-specific files for a node you do not own.

### Coordinate only through the repo and GitHub issues

- **Claim an issue** before you start: assign it to the human owner and comment that you are starting it. Do not start work that another agent has already claimed.
- Open small pull requests that link the issue (`Refs #12` or `Closes #12`).
- Never push `--force`, and never rewrite `main`.
- **Never edit the other node's host-specific files.** If a shared file must change, do it in a PR and leave the other node's sections alone.
- Do not close the other node's issues, and do not mark their verification done.

Host-specific files and sections:

- `inventory/hardware-inventory.md` — the Node A table vs the Node B table
- `inventory/network-inventory.md` — per-node rows
- `deployment/ansible/` host inventory and `host_vars/` for a single node (when they exist)
- Config or docs that name one hostname, one inventory, or "on Node A" / "on Node B" only

Shared files (`README.md`, `AGENTS.md`, `docs/architecture.md`, `docs/two-node-cluster.md`, example configs under `config/`, policy docs) may be edited by either agent via a PR.

Existing issues in M04–M14 were first written for a single server. Treat unlabelled ones as **Node A** unless they already have the `both` or `node-b` label. Node B's hardware inventory, OS-install tracker, AI-host tracker, and the M15 interconnect issues are the Node B / both-node work. If a later M04–M14 task must be done separately on Node B, open a `node-b` issue in the same milestone and link the Node A issue. Do not duplicate the whole board up front.

## Repo layout

```text
README.md                 Project overview
AGENTS.md                 This file
CLAUDE.md                 Short pointer here for Claude / T3
CONTRIBUTING.md           Team workflow
docs/                     Design and operations docs (English, except student-facing)
docs/two-node-cluster.md  How Node A and Node B talk
decisions/                Architecture Decision Records
inventory/                Hardware and network templates (placeholders only)
config/                   Example configs with placeholders
deployment/ansible/       Deployment-server examples
scripts/check-secrets.sh  Run this before every push
```

## Milestone order and the board

Work goes **M01 → M14**, then **M15 — Node Interconnect**. Do not skip ahead to installs before discovery, permission and design are done.

| Milestone | What it is |
| --- | --- |
| M01 | Discovery and inventory of **both** nodes |
| M02 | Approval and policy (AUP, logging, **which model to run**) |
| M03 | Architecture and design |
| M04 | OS installation (each node, by its owner) |
| M05 | Remote access |
| M06 | Security hardening |
| M07 | Users and access |
| M08 | GPU and drivers |
| M09 | AI host (inference engine on each node) |
| M10 | Web UI and API |
| M11 | Deployment Server (*sikkerhet*) |
| M12 | Testing |
| M13 | Benchmarking |
| M14 | Documentation and handover |
| M15 | Node interconnect (network, SSH trust, backend federation, failover) |

M15 depends on **both** nodes having an OS (M04) and an AI host (M09). Some M15 tasks also need the web UI (M10). Node roles (which machine runs Open WebUI, how backends are split) stay **TBD until both M01 inventories are done**.

Board: [AI Server — Development](https://github.com/users/ganya002/projects/5). Prefer issues already on the board over creating duplicates.

## Conventions

- Documentation is **English**, except student-facing text (AUP, student guide, banners), which is **Norwegian bokmål**.
- Small PRs and commits. Reference issue numbers: `Refs #12` or `Closes #12`.
- When you finish a task, update the relevant docs and, if it is in scope, [docs/acceptance-checklist.md](docs/acceptance-checklist.md).
- Write `TBD` for anything not known yet. Never guess school infrastructure.
- Use placeholders: `AI_SERVER_A_IP`, `AI_SERVER_B_IP`, `AI_NODE_A_HOSTNAME`, and documentation addresses `192.0.2.x`, `198.51.100.x`, `203.0.113.x`.

## How to use `gh`

The `gh` CLI is logged in as `ganya002` on Gabby's Mac. Typical commands:

```bash
gh issue list -R ganya002/school-ai-server --state open --limit 50
gh issue list -R ganya002/school-ai-server --label node-b --state open
gh issue view 12 -R ganya002/school-ai-server
gh issue comment 12 -R ganya002/school-ai-server --body "Starting this for Node A."
gh issue edit 12 -R ganya002/school-ai-server --add-assignee ganya002
gh issue close 12 -R ganya002/school-ai-server --reason completed --comment "Done. Evidence: …"
```

Move a board item when you change an issue's status (Ready → In Progress → Review / Testing → Done, or Blocked). If you cannot move the project card, comment the new status on the issue and leave the card.

Do not delete issues. Close as **not planned** (with a comment) only when a decision makes the issue irrelevant.

## Hard rules

This repository is **public**.

- Never commit secrets, passwords, API keys, tokens, `.env` files, SSH private keys, or model weights.
- Never commit real IP addresses, hostnames, MAC addresses, VLAN IDs, student names, or other school-internal details. Use placeholders and `*.example` files.
- Never run destructive disk commands, or wipe or partition either server, unless Gabby has explicitly approved that exact step for that machine.
- Never `git push --force` (or `--force-with-lease` to `main`).
- Anything that touches a real server (SSH, installs, firewall changes, service restarts) needs **Gabby's OK** first. Node B's human owner must also be in the loop for Node B.
- Do not pipe `curl` or `wget` into `sh`. Use official packages, signed releases, or a documented install you have reviewed.

If a secret lands in Git, stop and tell the project owner. The secret must be rotated; deleting the commit is not enough.

## Secret scan (no pre-commit hook)

Before every push:

```bash
./scripts/check-secrets.sh
```

The script scans the diff against `origin/main` (and the working tree) for private keys, credential assignments, and IPv4/MAC addresses outside the documentation ranges. Fix any hit before you push. You can also eyeball:

```bash
git diff origin/main | command grep -nE 'BEGIN (OPENSSH|RSA|EC) PRIVATE|password\s*=|api[_-]?key|secret[_-]?key|WEBUI_SECRET|[0-9]{1,3}(\.[0-9]{1,3}){3}'
```

## What an agent can do right now without hardware access

Many board issues are blocked on M01 inventory, teacher/IT, or a live machine. Do not mark those done. You **may** draft documentation and example configs, leave values as `TBD`, and open a PR that says it is a draft.

Concrete issues you can advance from this repo and public documentation alone (draft only until their blockers are done):

- **M02 policy:** [#28](https://github.com/ganya002/school-ai-server/issues/28) draft the student AUP (Norwegian). [#27](https://github.com/ganya002/school-ai-server/issues/27) licence checks once candidates are in [docs/model-selection.md](docs/model-selection.md) — do not choose the model yourself. Banner and system-prompt drafts for later teacher approval.
- **M03 architecture:** engine comparison in [docs/ai-host.md](docs/ai-host.md) (GPU numbers stay TBD); draft port/firewall matrix with placeholder IPs; role model in [docs/users-and-roles.md](docs/users-and-roles.md); refine diagrams; draft ADR options for secrets storage.
- **M06 hardening configs:** improve examples under `config/ssh`, `config/ufw`, `config/fail2ban`, `config/sudoers`, `config/unattended-upgrades`, and the structure of [docs/security-hardening.md](docs/security-hardening.md). Do not apply them to a server.
- **M10 web UI:** improve `config/open-webui/open-webui.env.example` and draft [docs/web-ui-and-api.md](docs/web-ui-and-api.md) and the Norwegian [docs/student-user-guide.md](docs/student-user-guide.md).
- **M12 test plans:** expand [docs/acceptance-checklist.md](docs/acceptance-checklist.md) and draft the test plan (including the A↔B checks in [docs/two-node-cluster.md](docs/two-node-cluster.md)).
- **M14 docs:** structure and expand operations, backup and troubleshooting guides. Do not invent incidents or results.
- **M15 interconnect (draft):** keep [docs/two-node-cluster.md](docs/two-node-cluster.md) accurate, with roles still TBD until both inventories exist. Example ufw allowlists and health-check commands may be drafted with placeholders.

Do not close issues that need teacher/IT sign-off, hardware evidence, or a live server.
