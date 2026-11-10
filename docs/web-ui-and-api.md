# Web UI & API

> Status: **Planned.** Open WebUI is the proposed web interface ([docs](https://docs.openwebui.com/)).

## 1. Installation (M10-001)

| Item | Value |
| --- | --- |
| Version | TBD |
| Method | TBD (Docker or Python, per ADR) |
| Data directory | TBD (persistent) |
| `WEBUI_SECRET_KEY` | In the secret store, never in Git |
| Connection to engine | TBD (`OLLAMA_BASE_URL` or OpenAI-compatible URL to 127.0.0.1) |
| TLS method | TBD (ADR M06-014) |

Example environment file: [`config/open-webui/open-webui.env.example`](../config/open-webui/open-webui.env.example). Variable reference: [env configuration](https://docs.openwebui.com/reference/env-configuration).

## 2. Accounts and permissions

See [users-and-roles.md](users-and-roles.md). Checklist:

- [ ] First admin account created immediately after install (the first account becomes admin).
- [ ] Open sign-up disabled or default role *pending*.
- [ ] Groups: admins, teachers, operators, students.
- [ ] Model access per group (approval conditions applied).
- [ ] Student permissions reviewed feature by feature.
- [ ] Banner and system prompt from the AUP ([banners](https://docs.openwebui.com/features/administration/banners)).

## 3. Rate limits (M02-011, M10-014)

| Limit | Initial value | After benchmarks |
| --- | --- | --- |
| Requests per minute per user | TBD | TBD |
| Max output tokens | TBD | TBD |
| Concurrent requests per user | TBD | TBD |
| Implementation method | TBD (e.g. Open WebUI filter function, reverse proxy limit, engine parallel limit) | |

## 4. API access

Open WebUI can issue per-user API keys ([docs](https://docs.openwebui.com/features/authentication-access/api-keys)). Allowed roles: TBD (default: not students).

```bash
# Example (placeholders; never paste real keys into issues)
curl -s https://AI_SERVER_HOSTNAME/api/chat/completions \
  -H "Authorization: Bearer $OPENWEBUI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL_ID","messages":[{"role":"user","content":"Hei!"}]}'
```

The inference engine's own API stays on `127.0.0.1` and is not exposed.
