# Challenge 08: Reuse one SSH connection

![One glowing SSH bridge carries several command sessions to the same lab server](../assets/challenge-08-multiplexing.png)

## Goal

Open one background SSH connection from your computer to the first Alpine target, run two commands through it, and close it. OpenSSH calls the background connection a **master** and the later commands **multiplexed sessions**.

## 1. Start the lab and open the master

On a fresh clone, `state/ssh_config` does not exist yet. Run **this entire block** from the playground directory; it starts the lab, creates that local config and a private socket directory, and then opens the SSH connection:

```bash
docker compose up -d
./lab doctor
./lab ssh-config > state/ssh_config
chmod 600 state/ssh_config
mkdir -p state/mux
chmod 700 state/mux
ssh -F state/ssh_config -M -S state/mux/playground.sock -fN playground
ssh -F state/ssh_config -S state/mux/playground.sock -O check playground
```

The config points `playground` at `learner@127.0.0.1:2222`, uses your generated console key, and checks the pinned server key. The final command should report a running master and its process ID. `-M` makes this connection the master; `-S` names its local control socket; `-fN` sends it to the background without running a remote command. The socket lives under Git-ignored `state/mux/` on your computer, not on the Alpine server. Keep working from the playground directory while using the relative socket path below.

## 2. Send two sessions through it

```bash
ssh -F state/ssh_config -S state/mux/playground.sock -o ControlMaster=auto playground 'whoami'
ssh -F state/ssh_config -S state/mux/playground.sock -o ControlMaster=auto playground 'hostname'
ssh -F state/ssh_config -S state/mux/playground.sock -O check playground
```

Expect `learner`, then the target's hostname, then the same master process ID. `ControlMaster=auto` tells each new SSH command to use the existing socket. Each command opens a new session over the already authenticated connection. Your console private key remains on your computer.

To see the reuse directly, add `-v` to either command in this section and look for a line containing `mux_client_request_session` in the diagnostic output.

## 3. Close it

```bash
ssh -F state/ssh_config -S state/mux/playground.sock -O exit playground
test ! -S state/mux/playground.sock && echo 'Control socket closed'
```

`-O exit` asks the background master to stop. Its socket should disappear. If you left the master running and need to reset the lab, run the exit command before `docker compose down`.

## n8n companion

After you create the n8n owner account, run `./lab setup-n8n` and refresh n8n. Open **SSH Playground - 08 - Credential Reuse** and execute it manually. The workflow has two SSH nodes, one printing the remote account and the next printing the remote hostname. Both use the **SSH Playground Automation** credential.

This companion shows how two n8n SSH nodes reuse one saved credential. n8n makes its own SSH connections from its container; it does not use the OpenSSH control socket on your computer. You can inspect the output of both nodes in the execution view.

## Explain what happened

- Which machine holds the control socket and the console private key?
- What does `-O check` tell you that `whoami` does not?
- How is reusing one OpenSSH connection different from reusing one n8n credential?

If a command fails, run `./lab doctor` and check the [troubleshooting guide](../docs/troubleshooting.md). Keep `state/` and its private keys out of screenshots and Git.
