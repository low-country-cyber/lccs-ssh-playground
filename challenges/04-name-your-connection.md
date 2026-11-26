# Challenge 04: Name your connection

![A learner turns connection details into one saved SSH shortcut to the protected lab server](../assets/challenge-04-ssh-config.png)

## Goal

Replace the long command from Challenge 02 with a memorable SSH host name. You will save the lab's settings in a file under the Git-ignored `state/` directory, inspect them, and connect with `ssh -F state/ssh_config playground`. Your personal `~/.ssh/config` does not need to change.

## 1. Start the lab

Work from the playground directory. If the lab isn't already running, start it now.

```bash
docker compose up -d
```

With the lab running, check that it's ready.

```bash
./lab doctor
```

Stay in the playground directory for the commands below.

## 2. Make a project-local SSH config

```bash
./lab ssh-config > state/ssh_config
chmod 600 state/ssh_config
cat state/ssh_config
```

The file should begin with `Host playground`. It also names the real host (`127.0.0.1`), user (`learner`), port (`2222`), generated private-key **path**, and pinned `known_hosts` file. It contains paths and settings, not the private key itself.

## 3. Use the short name

Run one remote command:

```bash
ssh -F state/ssh_config playground 'whoami && hostname'
```

The first output line should be `learner`; the next is the lab container's hostname. Then open a shell:

```bash
ssh -F state/ssh_config playground
```

Run `pwd` and `cat README.txt`, then type `exit`. The `-F` option tells OpenSSH to read this project-local config file. The name `playground` is an alias for the same `learner@127.0.0.1:2222` destination used earlier.

## 4. Change only the alias

Make a practice copy with a different host name:

```bash
sed 's/^Host playground$/Host alpine-lab/' state/ssh_config > state/ssh_config.practice
chmod 600 state/ssh_config.practice
ssh -F state/ssh_config.practice alpine-lab 'whoami'
```

The result should still be `learner`. You changed the name you type, not the server, user, port, or key. The original `state/ssh_config` still works.

## Explain what happened

- Which config line chooses the address, and which chooses the account?
- Why does this lesson use `-F state/ssh_config` instead of editing your personal SSH config?
- Does n8n use this host alias, or does its credential still connect to `ssh-target:22` inside Docker?

## n8n companion

After owner setup, run `./lab setup-n8n` once and refresh n8n. Open **SSH Playground - 04 - Alias Independence** and execute it manually. Its SSH connection still uses the n8n credential, regardless of what you named your host-terminal alias.

If the connection fails, run `./lab doctor` and check the [troubleshooting guide](../docs/troubleshooting.md). Keep `state/keys/console` private even though its path appears in the config.

Next, try [Challenge 05: Deliver a file](05-deliver-a-file.md) to use the same SSH shortcut with `scp` and `sftp`.
