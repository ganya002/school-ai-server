# Ansible (Deployment Server)

> Status: **Not started — scope depends on the teacher's clarification** (M03-002, M11-001). See [docs/deployment-server.md](../../docs/deployment-server.md). Target hosts are Windows 11 ([ADR 0001](../../decisions/0001-windows-11-native.md)); do not write Ubuntu/ufw roles as the plan.

Planned layout (create in M11):

```text
deployment/ansible/
├── inventory.example.ini     Placeholder inventory (the real inventory.ini is git-ignored)
├── ansible.cfg               (M11-002)
├── site.yml                  Applies the roles below
└── roles/
    ├── ssh-hardening/        (M11-005) same settings as config/ssh/10-hardening.conf.example
    ├── windows-firewall-baseline/  (M11-006) port matrix from docs/network.md
    ├── windows-update/       (M11-007) Windows Update baseline (not fail2ban)
    └── wazuh-agent/          (M11-014, only if Wazuh is in scope)
```

Rules:

- Real inventories, `host_vars/` and vault files are git-ignored.
- The deploy user's private key stays on the control node (mode 600) and is never committed.
- Every role must be idempotent: the second run reports no changes.
- Run with `--check --diff` first.

References: [Ansible getting started](https://docs.ansible.com/ansible/latest/getting_started/index.html) · [Inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html) · [Wazuh with Ansible](https://documentation.wazuh.com/current/deployment-options/deploying-with-ansible/index.html)
