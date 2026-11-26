# Challenge 02: Connect with OpenSSH

## Goal

Reach the Alpine SSH target from your host terminal using `ssh` directly. Challenge 01 used `./lab console`; here you supply the username, host, port, key, and host-key check yourself.

## Connect

Start the lab with `docker compose up -d` and run `./lab doctor`. From the playground directory, enter:

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

If the connection fails, use the [troubleshooting guide](../docs/troubleshooting.md). Keep the private key in `state/keys/console` local; never paste it into an issue or screenshot.
