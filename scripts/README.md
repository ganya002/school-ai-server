# Scripts

| Script | What it does | Changes the system? |
| --- | --- | --- |
| [`linux/collect-hardware-inventory.sh`](linux/collect-hardware-inventory.sh) | Prints CPU, RAM, GPU, disk and NIC facts for `inventory/hardware-inventory.md` | No (read-only) |
| [`benchmark/bench_openai.py`](benchmark/bench_openai.py) | Measures tokens/sec and time-to-first-token against an OpenAI-compatible endpoint | No |
| [`check-secrets.sh`](check-secrets.sh) | Scans the git diff for secrets and real IPs/MACs before a push | No |

None of the inventory or benchmark scripts have been run on the real servers yet. Run `check-secrets.sh` before every push.
