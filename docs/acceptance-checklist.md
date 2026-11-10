# Acceptance Checklist

> Run in M12-013. Each item: pass / fail + link to evidence. Failures become bug issues.

## Approval & policy
- [ ] Written teacher + IT decision on the abliterated model is recorded (ADR).
- [ ] The deployed model matches the decision (abliterated or official fallback).
- [ ] AUP approved and shown to students (banner).
- [ ] Logging and retention match the policy.

## OS & remote access
- [ ] Ubuntu Server LTS installed and fully updated.
- [ ] SSH key-only, no root login, AllowGroups.
- [ ] Remote access only through the approved private path.
- [ ] No port reachable from the internet (IT confirmation).
- [ ] Console access documented and tested.

## Security
- [ ] ufw default deny; open ports match the port matrix from each network.
- [ ] fail2ban active and tested.
- [ ] unattended-upgrades active.
- [ ] Lynis baseline recorded; warnings fixed or accepted.
- [ ] Inference API only on 127.0.0.1.

## Users & access
- [ ] Personal accounts only; no shared accounts.
- [ ] sudo rights per role tested.
- [ ] Web UI: no open sign-up; groups and model access per role.
- [ ] Student test account cannot reach admin functions.
- [ ] API keys only for permitted roles.

## AI host
- [ ] Model runs fully on the GPU (or offload documented).
- [ ] Services restart after failure and after reboot.
- [ ] Three concurrent users served.
- [ ] Rate limit works.
- [ ] Fallback model switch tested.

## Deployment server (scope per teacher)
- [ ] Scope ADR accepted.
- [ ] Hardening playbook is idempotent and hardens a test target.
- [ ] (If in scope) Wazuh agent enrolled and SSH failures alert.

## Handover
- [ ] Backups taken and restore tested.
- [ ] Operations, troubleshooting and student guides complete.
- [ ] Admin access handed over to teacher/IT.
- [ ] Teacher sign-off.
