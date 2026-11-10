# Ansible (Deployment Server)

> Status: **Not started — scope depends on the teacher's clarification** (M03-002, M11-001). See [docs/deployment-server.md](../../docs/deployment-server.md).

Planned layout (create in M11):

```text
deployment/ansible/
├── inventory.example.ini     Placeholder inventory (the real inventory.ini is git-ignored)
├── ansible.cfg               (M11-002)
├── site.yml                  Applies the roles below
└── roles/
    ├── ssh-hardening/        (M11-005) same settings as config/ssh/10-hardening.conf.example
    ├── ufw-baseline/         (M11-006) port matrix from docs/network.md
    ├── updates-fail2ban/     (M11-007)
    └── wazuh-agent/          (M11-014, only if Wazuh is in scope)
```

Rules:

- Real inventories, `host_vars/` and vault files are git-ignored.
- The deploy user's private key stays on the control node (mode 600) and is never committed.
- Every role must be idempotent: the second run reports no changes.
- Run with `--check --diff` first.

References: [Ansible getting started](https://docs.ansible.com/ansible/latest/getting_started/index.html) · [Inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html) · [Wazuh with Ansible](https://documentation.wazuh.com/current/deployment-options/deploying-with-ansible/index.html)
