# Bundled n8n workflows

After creating the lab's n8n owner account, run `./lab setup-n8n` from the repository directory. It imports three SSH credentials and every numbered JSON workflow here. Refresh n8n, open a workflow, and run it manually. All workflows are imported inactive.

| Files | SSH destination | Credential |
| --- | --- | --- |
| `01` through `06`, `08` through `10` | First target, `ssh-target:22` | SSH Playground Automation |
| `07` | Hidden target, `hidden-target:22` | SSH Playground Hidden Automation |
| `11` | First target, `ssh-target:22` | SSH Playground Report Only for the first node; SSH Playground Automation for the verification node |

The JSON templates contain no private keys or n8n credential IDs. The `labCredential` marker on an SSH node selects a lab destination; `scripts/setup-n8n.py` removes that marker and binds the matching credential during import. If you import a JSON file manually in n8n, open its SSH node and select the matching credential yourself.

Workflow `10` needs the host web server and reverse SSH tunnel from [Challenge 10](../challenges/10-share-a-host-page.md) running when you execute it. The other bundled workflows do not depend on a host-terminal tunnel. Workflow `11` uses the [restricted key](../challenges/11-restrict-one-key.md) to show that a successful SSH connection can still ignore the client's requested command.
