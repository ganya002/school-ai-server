# Users & Roles

> Status: **Planned.** Proposed role model; confirmed in M03-013. No student names or personal data are stored in this repository.

## 1. Identity source (M01-019, M03-014)

| Item | Value |
| --- | --- |
| School identity systems (Feide / Entra ID / AD / LDAP) | TBD |
| May the project integrate with them? | TBD |
| Web UI account method | TBD (default: admin-created accounts or sign-up as *pending* approved by an admin) |

## 2. Linux roles (proposed)

| Group | Who | SSH | sudo | Notes |
| --- | --- | --- | --- | --- |
| `ai-admins` | Team admins, later teacher/IT | Yes (key) | Full | [`config/sudoers/ai-admins.example`](../config/sudoers/ai-admins.example) |
| `ai-operators` | Team members / teacher who restart services | Yes (key) | Only listed service/log commands | [`config/sudoers/ai-operators.example`](../config/sudoers/ai-operators.example) |
| `ai-students` | Only if shell access is approved (default: **not created**) | No by default | None | M07-003 |
| service user (e.g. `ollama`) | Inference engine | No login | None | M09-001 |
| deploy user | Ansible (if in scope) | Key, from control node only | As needed | M11-004 |

## 3. Web UI roles (Open WebUI)

Open WebUI has the roles **admin**, **user** and **pending**; the first account created becomes admin ([docs](https://docs.openwebui.com/features/authentication-access/rbac/roles)). Groups and permissions refine access ([groups](https://docs.openwebui.com/features/authentication-access/rbac/groups), [permissions](https://docs.openwebui.com/features/authentication-access/rbac/permissions)).

| Group | Role | Models | Features | API keys |
| --- | --- | --- | --- | --- |
| admins | admin | All | All | Yes |
| teachers | user | TBD (all approved) | TBD | TBD |
| operators | user | TBD | TBD | TBD |
| students | user | Only approved for students (approval ADR) | Chat; others TBD (M10-009) | TBD (default no) |

## 4. Permission tests (M07-007)

| Role | Command / action | Expected | Actual |
| --- | --- | --- | --- |
| ai-admins | `sudo -v` | allowed | TBD |
| ai-operators | `sudo systemctl restart <engine>` | allowed | TBD |
| ai-operators | `sudo -i` | denied | TBD |
| non-member | SSH login | denied | TBD |

## 5. Directory permissions (M07-010)

| Path | Owner:group | Mode |
| --- | --- | --- |
| model directory | TBD | TBD |
| engine config | TBD | TBD |
| web UI data | TBD | TBD |

## Onboarding and offboarding

TBD (M07-013). Must include: account, group, SSH key, web UI account, secret-store access; on offboarding: remove keys, lock account, rotate shared secrets.

## SSO / LDAP (research, M07-014)

Status: **TBD.** Open WebUI supports [LDAP](https://docs.openwebui.com/features/authentication-access/auth/ldap) and [SSO/OIDC](https://docs.openwebui.com/features/authentication-access/auth/sso/). Use with [Feide](https://www.feide.no/) or Entra ID only if school IT allows it.
