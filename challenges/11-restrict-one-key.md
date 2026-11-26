# Challenge 11: Restrict one key

![A learner sends a shielded SSH key to a server that returns only a fixed report](../assets/challenge-11-restricted-key.png)

## Goal

Use two different keys for the **same** `automation` account. One runs ordinary commands. The other is limited to a fixed report, even when a client asks it to run something else. You will verify the restriction from your terminal and then see it in n8n.

The commands use `~/lccs-ssh-playground`, the folder created by the README Quick Start. If you cloned elsewhere, use that folder in the `cd` line.

## 1. Start a fresh lab

```bash
cd ~/lccs-ssh-playground
docker compose up -d
./lab doctor
```

The helper checks the ordinary login, the restricted key, and n8n health. Stay in this directory for the rest of the challenge.

## 2. Ask the same account to run two commands

```bash
./lab automation 'whoami'
./lab report 'whoami'
./lab report 'hostname'
```

The first command returns `automation`. The next two return the **same fixed report** with the account and target named inside it. The `report` helper still connects as `automation`, but it presents `state/keys/report-only`. SSH ignores the requested `whoami` or `hostname` when that key is used.

## 3. Inspect the server's two public-key rules

```bash
awk '{print $1}' state/server/automation_authorized_keys
```

The first line starts with `ssh-ed25519`: it is the ordinary automation key. The second starts with `restrict,command="/usr/local/bin/lab-report.sh"`: these options apply **only to that public key**. The `command=` option runs the fixed script regardless of the command requested by the client. `restrict` also blocks a terminal allocation and forwarding for that key. You can inspect [the report script](../scripts/lab-report.sh) to see the exact commands it runs. This `awk` command prints only the first field of each line, so it does not display the public-key material.

## 4. Prove the requested write did not run

The following request names a harmless file **inside the disposable Alpine target**:

```bash
./lab report 'touch /tmp/lccs-playground-11-should-not-exist'
./lab automation 'test ! -e /tmp/lccs-playground-11-should-not-exist && echo "No file created"'
```

You should see the fixed report, then `No file created`. The second check uses the ordinary automation key to independently inspect the target. A successful SSH connection with the restricted key means the fixed report ran; it does **not** mean the requested `touch` ran.

## n8n companion

After creating the lab's owner account at [http://localhost:5680](http://localhost:5680), run `./lab setup-n8n` from the playground directory and refresh n8n. Open **SSH Playground - 11 - Restricted Key** and execute it manually.

The first SSH node asks for the same harmless `touch`, using **SSH Playground Report Only**. Its output should be the fixed report. The second SSH node uses **SSH Playground Automation** to verify `No file created`. The workflow shows why the key selected in an n8n SSH credential matters even when both credentials use the same username and server.

## Explain what happened

- Which key let `automation` run `whoami` normally?
- Why did the `touch` request return a success report without creating a file?
- Where is the restriction enforced: in the n8n workflow, the SSH client, or the server's `authorized_keys` entry?

This restriction is per key. Earlier workflows still use the ordinary automation key, so they can run their commands. Keep the generated private keys in `state/` and out of screenshots and Git. If the restricted key returns `Permission denied (publickey)`, run `./lab doctor` and use the [troubleshooting guide](../docs/troubleshooting.md).
