# Challenge 07: Reach a hidden SSH target

![A learner reaches a hidden SSH server through a guarded jump host](../assets/challenge-07-proxyjump.png)

## Goal

Connect from your terminal to a second Alpine SSH server that has no published host port. The first server will act as a jump host. You will still authenticate to the hidden server with a key on **your computer**, and you will verify its own host key.

## 1. Prepare the SSH config

Work from the playground directory. If the lab isn't already running, start it now.

```bash
docker compose up -d
```

Run the following block even if the lab was already running. It checks the lab and creates `state/ssh_config` with both the first server and the hidden target.

```bash
./lab doctor
./lab ssh-config > state/ssh_config
./lab jump-config >> state/ssh_config
chmod 600 state/ssh_config
```

The first config block names `playground`, the server reachable at `127.0.0.1:2222`. The second names `hidden-lab` and adds `ProxyJump playground`. Both blocks use paths under the Git-ignored `state/` directory. `./lab jump-config` prints settings; it does not copy a key to either server.

## 2. See the route you configured

```bash
ssh -G -F state/ssh_config hidden-lab | grep -E '^(hostname|user|port|proxyjump|hostkeyalias) '
docker compose ps
```

Look for `hostname hidden-target`, `user learner`, `port 22`, and `proxyjump playground`. In the Compose output, `hidden-target` has no port published on your computer. The name `hidden-target` resolves inside the Compose network, where the jump host lives.

## 3. Connect through the jump host

```bash
ssh -F state/ssh_config hidden-lab 'whoami && hostname && cat README.txt'
```

Expect `learner`, then `hidden-lab`, then a line beginning **LCCS SSH Playground: Hidden Target**. You can also run `ssh -F state/ssh_config hidden-lab` for an interactive shell; type `exit` to return home.

`ProxyJump` makes one SSH connection to `playground` and forwards the next connection through it to `hidden-target:22`. The hidden target authenticates your console key and presents its own host key. The jump host forwards traffic; it does not need your private key.

## 4. Transfer through the same route

```bash
printf 'LCCS SSH Playground two-hop note\n' > state/jump-note.txt
scp -F state/ssh_config state/jump-note.txt hidden-lab:jump-note.txt
ssh -F state/ssh_config hidden-lab 'cat jump-note.txt'
```

The final command should print the note. `scp` uses the same `hidden-lab` settings, including the jump host.

## 5. Check the two server identities

```bash
ssh-keygen -lf state/server/ssh_host_ed25519_key.pub
ssh-keygen -lf state/hidden-server/ssh_host_ed25519_key.pub
ssh -F state/ssh_config playground 'ls -l ~/.ssh'
```

The two SHA256 host fingerprints should differ because these are separate servers. The jump host's `~/.ssh` contains an `authorized_keys` file for your public key, but no copy of your console private key. Your client checks the hidden server against `state/hidden_known_hosts`.

## n8n companion

You can run this after finishing the command line lessons. Create the n8n owner account if needed, run `./lab setup-n8n`, and refresh n8n. Open **SSH Playground - 07 - Hidden Target** and execute it manually. Expect `automation`, `hidden-lab`, and the hidden target's README text.

n8n uses the separate **SSH Playground Hidden Automation** credential. Because n8n is already on the Compose network, its SSH node connects directly to `hidden-target:22`; the host-terminal exercise uses `ProxyJump` to reach that same server.

## Explain what happened

- Which machine has your console private key during the two-hop connection?
- Why does the hidden target need its own host key entry?
- Why does n8n connect to `hidden-target:22` directly while your host terminal uses a jump?

If the connection fails, run `./lab doctor`, check both `ssh-target` and `hidden-target` in `docker compose ps`, and use the [troubleshooting guide](../docs/troubleshooting.md). Keep generated private keys in `state/` and out of screenshots and Git.

Next: [Challenge 08: Reuse one SSH connection](08-reuse-one-connection.md).
