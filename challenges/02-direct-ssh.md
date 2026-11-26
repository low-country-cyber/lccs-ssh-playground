# Challenge 02: Connect with OpenSSH

![A learner connects directly from a terminal through an SSH key and port to the Alpine lab server](../assets/challenge-02-direct-ssh.png)

## Goal

Reach the Alpine SSH target from your host terminal using `ssh` directly. Challenge 01 used `./lab console`; here you supply the username, host, port, key, and host-key check yourself.

## Connect

Work from the playground directory. If the lab isn't already running, start it with `docker compose up -d`. Run `./lab doctor` to check the lab. Then enter the SSH command below.

```bash
ssh -p 2222 \
  -i ./state/keys/console \
  -o IdentitiesOnly=yes \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=./state/known_hosts \
  learner@127.0.0.1
```

You should land in the lab's Alpine shell. Run `whoami`, `hostname`, and `cat README.txt`, then type `exit` to return to your host terminal.

| Part | Meaning |
| --- | --- |
| `learner@127.0.0.1` | Log in as `learner` through your own computer's loopback address |
| `-p 2222` | Use the port Docker publishes on the host; the container listens on port `22` |
| `-i ./state/keys/console` | Use the generated learner private key |
| `IdentitiesOnly=yes` | Offer this key instead of other keys from your SSH agent |
| `StrictHostKeyChecking=yes` | Refuse an unrecognized or changed server key |
| `UserKnownHostsFile=./state/known_hosts` | Check the server key pinned when the lab was initialized |

`learner@127.0.0.1:2222` describes the destination, but it is **not** the command syntax. OpenSSH takes the port with `-p 2222` and the destination as `learner@127.0.0.1`.

## Run a command without opening a shell

Use the same connection settings, then put the remote command after the destination:

```bash
ssh -p 2222 \
  -i ./state/keys/console \
  -o IdentitiesOnly=yes \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=./state/known_hosts \
  learner@127.0.0.1 'whoami && hostname'
```

The first line of output should be `learner`; the second is the lab container's hostname. You stay at your host prompt because SSH closes after the command finishes.

## Explain what happened

- Which part of the command identifies the account, and which part selects the host port?
- What would `ssh` do if the server key no longer matched `state/known_hosts`?
- Why does n8n use `ssh-target:22` while your host terminal uses `127.0.0.1:2222`?

## n8n companion

After owner setup, run `./lab setup-n8n` once and refresh n8n. Open **SSH Playground - 02 - Connection Routes** and execute it manually. It reaches the same target as `automation` through the Compose network.

If the connection fails, use the [troubleshooting guide](../docs/troubleshooting.md). Keep the private key in `state/keys/console` local; never paste it into an issue or screenshot.

Next, try [Challenge 03: Who trusts whom?](03-who-trusts-whom.md) to see why your key works for `learner` and how your terminal recognizes the server.
