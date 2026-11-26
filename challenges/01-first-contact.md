# Challenge 01: First Contact

![A learner and an n8n automation connect to the same protected SSH lab server](../assets/ssh-playground-hero.png)

## Goal

Reach the same disposable SSH target from two places: your terminal and an n8n workflow. The terminal uses the `learner` identity. n8n uses the `automation` identity.

## Terminal route

Start the lab with `docker compose up -d`, then run `./lab doctor`. Open the learner shell with `./lab console` and run:

```sh
whoami
hostname
cat README.txt
```

Type `exit` when done. The generated `state/known_hosts` file pins the lab server's public host key, so the helper refuses an unexpected host key.

## n8n route

Create the owner account at `http://localhost:5680`, then run `./lab setup-n8n` from the playground directory and refresh n8n. Open **SSH Playground - First Contact** from the workflow list and execute it manually. The setup command imports all bundled workflows with their SSH credential already selected.

The expected first output line is `automation`. The second line is the lab target's hostname. The workflow is inactive until you choose to run it.

## Explain what happened

- Why does the terminal connect to `127.0.0.1` on port `2222`, while n8n connects to `ssh-target` on port `22`?
- Which machine holds each private key? Which machine accepts the matching public key?
- What should happen if the SSH target presents an unexpected host key?

Next, try [Challenge 02: Connect with OpenSSH](02-direct-ssh.md) to make the same terminal connection without the helper.
