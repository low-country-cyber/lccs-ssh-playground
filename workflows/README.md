# Bundled n8n workflows

After creating the lab's n8n owner account, run `./lab setup-n8n` from the repository directory. It imports the two SSH credentials and every numbered JSON workflow here. Refresh n8n, open a workflow, and run it manually. All workflows are imported inactive.

| Files | SSH destination | Credential |
| --- | --- | --- |
| `01` through `06` | First target, `ssh-target:22` | SSH Playground Automation |
| `07` | Hidden target, `hidden-target:22` | SSH Playground Hidden Automation |

The JSON templates contain no private keys or n8n credential IDs. The `labCredential` marker on an SSH node selects a lab destination; `scripts/setup-n8n.py` removes that marker and binds the matching credential during import. If you import a JSON file manually in n8n, open its SSH node and select the matching credential yourself.
