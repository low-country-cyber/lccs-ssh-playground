# Challenge 03: Who trusts whom?

![A learner compares two client key identities with the protected SSH server's identity](../assets/challenge-03-key-trust.png)

## Goal

Find the three SSH identities in this lab: your terminal's `learner` key, n8n's `automation` key, and the server's host key. See what happens when a valid key is offered to the wrong account. You will inspect public keys and fingerprints; you do not need to display a private key.

## 1. Start the lab

From a fresh clone of the playground, run:

```bash
docker compose up -d
./lab doctor
```

Stay in the playground directory for the rest of this challenge. `./lab doctor` should confirm both SSH logins and n8n health before you try the deliberate failure below.

## 2. Find the two client identities

```bash
ssh-keygen -lf state/keys/console.pub
ssh-keygen -lf state/keys/automation.pub
```

You should see **different** SHA256 fingerprints. The `.pub` files are public keys. The matching files without `.pub` are private keys: `state/keys/console` stays with your terminal, while `state/keys/automation` is imported into the lab's n8n credential.

## 3. See which public key each account accepts

```bash
cmp -s state/keys/console.pub state/server/learner_authorized_keys && echo 'learner accepts the console key'
cmp -s state/keys/automation.pub state/server/automation_authorized_keys && echo 'automation accepts the automation key'
```

Both messages should appear. The files under `state/server/` are the public-key lists prepared for the SSH target. At startup, the target installs them as each account's `authorized_keys` file. It never receives the client private-key directory.

## 4. Offer the wrong key

Try the automation key with the `learner` account:

```bash
ssh -p 2222 \
  -i ./state/keys/automation \
  -o BatchMode=yes \
  -o IdentitiesOnly=yes \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=./state/known_hosts \
  learner@127.0.0.1 'whoami'
```

Expect `Permission denied (publickey)`. Nothing is broken: the key is valid for `automation`, but `learner` does not authorize it. Confirm the correct identity still works:

```bash
./lab console 'whoami'
```

The result should be `learner`.

## 5. Check the server's identity

```bash
ssh-keygen -lf state/server/ssh_host_ed25519_key.pub
ssh-keygen -lf state/known_hosts
```

These should show the **same** SHA256 fingerprint. The first file is the server's public host key. The second pins that key to `[127.0.0.1]:2222` for your terminal. A server host key answers “which server am I reaching?”; a client key answers “which account may I use?”

## 6. Connect this to n8n

To try the automation identity in n8n:

1. Open `http://localhost:5680` and create the owner account if this is a fresh lab.
2. From the playground directory, run `./lab import-credential`, then refresh n8n.
3. Import [`workflows/01-first-contact.json`](../workflows/01-first-contact.json), choose **SSH Playground Automation** in its SSH node, and run it manually. The output should begin with `automation`.

```bash
./lab credential-info
```

This prints the connection fields and the **path** to n8n's automation key, without printing the private key. n8n uses `automation@ssh-target:22`; your terminal uses `learner@127.0.0.1:2222`. The different hostnames and ports are the Docker-internal and host-facing routes to the same SSH target.

## Explain what happened

- Why did the automation key fail for `learner` even though it is a valid lab key?
- Which files contain public keys, and where do the two client private keys stay?
- Why must your SSH client check the server's host key before it sends a login attempt?

Keep private keys out of screenshots, chat, and GitHub. If the expected results differ, see [troubleshooting](../docs/troubleshooting.md).

Next, try [Challenge 04: Name your connection](04-name-your-connection.md) to turn the long SSH command into a project-local shortcut.
