# Users & Roles

> Status: **Planned.** Proposed role model; confirmed in M03-013. No student names or personal data are stored in this repository. Host accounts are **Windows local accounts** (or domain accounts if IT later approves), not Linux users ([ADR 0001](../decisions/0001-windows-11-native.md)).

## 1. Identity source (M01-019, M03-014)

| Item | Value |
| --- | --- |
| School identity systems (Feide / Entra ID / AD / LDAP) | TBD |
| May the project integrate with them? | TBD |
| Web UI account method | TBD (default: admin-created accounts or sign-up as *pending* approved by an admin) |

## 2. Windows host roles (proposed)

| Group | Who | SSH | Elevation | Notes |
| --- | --- | --- | --- | --- |
| `ai-admins` (local group) | Team admins, later teacher/IT | Yes (key) | Full local admin, or an equivalent | Adapt [`config/sudoers/ai-admins.example`](../config/sudoers/ai-admins.example) to Windows group membership; do not assume sudo |
| `ai-operators` (local group) | Team members / teacher who restart services | Yes (key) | Only listed service/log actions (service ACL or a scheduled task) | Adapt the operators example the same way |
| `ai-students` | Only if shell access is approved (default: **not created**) | No by default | None | M07-003 |
| service account (e.g. for Ollama) | Inference engine | No login | None | M09-001 |
| deploy account | Ansible (if in scope) | Key, from control node only | As needed | M11-004 |

Linux sudoers examples under `config/sudoers/` are reference for *who may do what*, not files to copy onto these PCs.

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
| ai-admins | elevate / manage services | allowed | TBD |
| ai-operators | restart the inference service | allowed | TBD |
| ai-operators | an unbounded admin action | denied | TBD |
| non-member | SSH login | denied | TBD |

## 5. Directory permissions (M07-010)

| Path | Owner / ACL | Notes |
| --- | --- | --- |
| model directory | TBD | On an existing volume; do not create a new partition |
| engine config | TBD | TBD |
| web UI data | TBD | TBD |

## Onboarding and offboarding

TBD (M07-013). Must include: account, group, SSH key, web UI account, secret-store access; on offboarding: remove keys, lock account, rotate shared secrets.

## SSO / LDAP (research, M07-014)

Status: **TBD.** Open WebUI supports [LDAP](https://docs.openwebui.com/features/authentication-access/auth/ldap) and [SSO/OIDC](https://docs.openwebui.com/features/authentication-access/auth/sso/). Use with [Feide](https://www.feide.no/) or Entra ID only if school IT allows it.
