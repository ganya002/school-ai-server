# Contributing

How the team (max 3 students) works on the School AI Server.

Coding agents (DeepSeek, Claude, Cursor, and others) should also read [AGENTS.md](AGENTS.md).

## 1. Pick a task from the board

1. Open the [project board](README.md) and look in the **Ready** column.
2. Pick **one** issue and assign it to yourself. One owner per issue.
3. Move it to **In Progress**.
4. If you are waiting on something outside the team (IT, teacher, hardware), move it to **Blocked** and comment what you are waiting for.
5. When done, add the evidence asked for under **Verification** and move it to **Review / Testing**.
6. Another team member checks the evidence, then moves it to **Done** and closes it.

An issue only counts as finished when **all** acceptance criteria are ticked.

### Board statuses

| Status | Meaning |
| --- | --- |
| Backlog | Planned; prerequisites are still open |
| Ready | All prerequisites done; anyone can start |
| In Progress | Someone is working on it |
| Blocked | Waiting on something outside the team |
| Review / Testing | Done; waiting for a second person to verify |
| Done | Verified and closed |

### Dependencies

Each issue lists its prerequisites under **Prerequisites** and, where GitHub supports it, as native "blocked by" relationships. When an issue is closed, check which issues it unblocked and move them from Backlog to Ready.

### "Only if" tasks

Some tasks only apply to one path (e.g. *(VM path)* or *only if Docker was chosen*). When a decision makes them irrelevant, close them as **not planned** with a link to the decision.

## 2. Creating new issues

- Use the templates: **Task**, **Research**, **Decision** or **Bug**.
- One clear outcome, about 15–90 minutes, one person.
- Set the milestone, the Priority/Phase/Effort fields and at least one area label.

## 3. Branches and pull requests

- Branch name: `<issue-number>-short-description`, e.g. `42-firewall-port-matrix`.
- Small commits and pull requests. Reference the issue in the message, e.g. `Refs #12` or `Closes #12`.
- Open a pull request that links the issue (`Closes #42`).
- A second team member reviews every pull request.
- Never force-push to `main`.
- Before you push, scan the diff for secrets and real addresses:

  ```bash
  ./scripts/check-secrets.sh
  ```

## 4. Decisions

Record important decisions as ADRs in [`decisions/`](decisions/) using [`0000-template.md`](decisions/0000-template.md).

## 5. What may be committed

**Never commit:**

- Passwords, API keys, tokens, Open WebUI `WEBUI_SECRET_KEY`, VPN/Tailscale auth keys
- SSH private keys (`id_*`, `*.pem`, `*.key`)
- `.env` files (commit `*.example` files with placeholders instead)
- Model weights (`*.gguf`, `*.safetensors`, `*.bin`, …): they are downloaded on the server
- Databases (`*.db`, `*.sqlite`), chat exports or logs containing student data
- Student names, lists of student accounts or any other personal data

**This repository is public.** Infrastructure details (hostnames, IP addresses, MAC addresses, VLANs, usernames): **do not commit real values.** Agree with school IT what, if anything, may ever be stored here (M01 task *Agree which infrastructure details may be committed to the repository*). Until then — and by default — use placeholders such as `AI_SERVER_HOSTNAME`, `AI_SERVER_IP`, `ADMIN_VPN_RANGE`, `STUDENT_NET_RANGE`, and documentation IPs from [RFC 5737](https://datatracker.ietf.org/doc/html/rfc5737) (`192.0.2.x`, `198.51.100.x`, `203.0.113.x`).

**Change requests to school IT:** process TBD (M01 task *Identify the school IT contact for the AI server*).

**Where secrets live:** TBD (M03 decision *Decide where secrets are stored outside Git*).

If a secret is committed by accident, tell the project owner and school IT immediately. The secret must be **rotated**; deleting the commit does not make it safe.

## 6. Writing documentation

- Write documentation in **English**, except student-facing text (AUP, student guide, banners), which is **Norwegian bokmål** (English optional alongside).
- Write `TBD` for anything not known yet. Never guess school infrastructure details.
- When you finish a task, update the relevant docs and, if the change is in scope, [docs/acceptance-checklist.md](docs/acceptance-checklist.md).
- Link official documentation (Windows 11, NVIDIA, Ollama for Windows / llama.cpp, Open WebUI, Hugging Face model cards, Ansible, Wazuh).
- Only record results that someone actually measured or observed.
