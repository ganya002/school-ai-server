# Deployment Server (Sikkerhet)

> Status: **Waiting for clarification.** The assignment says the system should "act as a Deployment Server in security", but does not define it. Milestone M11 is planned for the most plausible interpretation and **depends on the teacher's answer** (M03-002).

## 1. Existing school tooling (M01-020)

| Tool | In use at school? | May we connect? |
| --- | --- | --- |
| Wazuh | TBD | TBD |
| Splunk | TBD | TBD |
| Other SIEM | TBD | TBD |
| Ansible / other config management | TBD | TBD |

## 2. Possible meanings (M03-001)

| Option | What it is | What we would show | Official docs | Fit with this server |
| --- | --- | --- | --- | --- |
| **A. Automation deployment server** | An Ansible control node that pushes hardened configuration (OpenSSH, Windows Firewall, updates) to machines over SSH | Playbooks that harden this server and a test target identically | [Ansible](https://docs.ansible.com/ansible/latest/getting_started/index.html) | Light; no extra services |
| **B. SIEM / agent deployment** | A Wazuh manager that collects security events, plus agents deployed to machines | Agents enrolled, alerts for SSH failures | [Wazuh quickstart](https://documentation.wazuh.com/current/quickstart.html), [agent](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/index.html) | Central components need significant RAM/CPU; may compete with the AI workload |
| **C. Splunk "Deployment Server"** | A Splunk Enterprise feature that distributes apps/configs to Splunk forwarders ("deployment clients") | Forwarders receiving config from the server | [Splunk: update your deployment](https://help.splunk.com/en/splunk-enterprise/administer/update-your-deployment/) | Needs Splunk licence/infrastructure; only if the school uses Splunk |
| D. Something else | e.g. PXE/OS deployment, WSUS-like update server | TBD | TBD | TBD |

**Working assumption (not yet confirmed):** A + B — Ansible deploys hardened configs and the Wazuh agent; the Wazuh manager runs where M11-011 decides.

## 3. Teacher's clarification (M03-002)

| Question | Answer |
| --- | --- |
| Which option(s) are expected | TBD |
| Which target machines | TBD |
| What must be demonstrated | TBD |

## 4. Implementation (M11, only for the confirmed scope)

| Part | Status |
| --- | --- |
| Ansible control node | Not started |
| Example inventory: [`deployment/ansible/inventory.example.ini`](../deployment/ansible/inventory.example.ini) | Placeholder |
| Roles: ssh-hardening, windows-firewall-baseline, windows-update, wazuh-agent | Not started |
| Wazuh manager location | TBD (ADR) |
| Test target | TBD |

## 5. How to add a new target (fill in after M11)

TBD.
