# Acceptance Checklist

> Run in M12-013. Each item: pass / fail + link to evidence. Failures become bug issues.

## Approval & policy
- [ ] Written teacher + IT decision on which model to run is recorded (ADR).
- [ ] The deployed model matches the decision.
- [ ] AUP approved and shown to students (banner).
- [ ] Logging and retention match the policy.

## OS & remote access
- [ ] Both nodes still run the original Windows 11 install (ADR 0001); the baseline (updates, drivers, power plan, timezone) is complete.
- [ ] OpenSSH Server: key-only, no Administrator SSH login, allowed groups/users only.
- [ ] Remote access only through the approved private path.
- [ ] No port reachable from the internet (IT confirmation).
- [ ] Physical console access documented and tested.

## Security
- [ ] Windows Defender Firewall: inbound default block; open ports match the port matrix from each network.
- [ ] Brute-force protection for SSH is in place and tested (Windows lockout / OpenSSH settings).
- [ ] Windows Update is active; the reboot policy is documented.
- [ ] A Windows security baseline is recorded; leftover findings are fixed or accepted.
- [ ] Inference API only on 127.0.0.1 (and, if needed, the peer node).

## Users & access
- [ ] Personal accounts only; no shared accounts.
- [ ] Local admin / operator rights per role tested.
- [ ] Web UI: no open sign-up; groups and model access per role.
- [ ] Student test account cannot reach admin functions.
- [ ] API keys only for permitted roles.

## AI host
- [ ] Model runs fully on the GPU (or offload documented).
- [ ] Services restart after failure and after reboot (Windows service or Task Scheduler).
- [ ] Three concurrent users served.
- [ ] Rate limit works.
- [ ] Switching to another approved model is tested (if a second model is installed).

## Deployment server (scope per teacher)
- [ ] Scope ADR accepted.
- [ ] Hardening playbook is idempotent and hardens a test target.
- [ ] (If in scope) Wazuh agent enrolled and SSH failures alert.

## Two-node interconnect
- [ ] Both nodes inventoried and on the same LAN/VLAN (placeholders in Git).
- [ ] SSH key trust and Windows Firewall allowlists between Node A and Node B are in place.
- [ ] Each inference backend is reachable from the web UI / proxy node and not from the public internet.
- [ ] A↔B connectivity and failover tests in docs/two-node-cluster.md have passed.

## Handover
- [ ] Backups taken and restore tested.
- [ ] Operations, troubleshooting and student guides complete.
- [ ] Admin access handed over to teacher/IT.
- [ ] Teacher sign-off.
