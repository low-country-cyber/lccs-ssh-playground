# LCCS SSH Playground

![An illustrated learner terminal and automation flow connecting to one isolated SSH lab server](assets/ssh-playground-hero.png)

**Learn SSH by doing it.** Start a disposable lab with one Docker Compose command, connect from your terminal, then run the same task from n8n. The first challenge is **First Contact**. No remote server or existing n8n account is required.

| What starts | Where you reach it |
| --- | --- |
| SSH lab target | Your terminal connects to `127.0.0.1:2222` |
| Hidden SSH target | Reach it through the first target with `ProxyJump`; no host port is published |
| Private n8n learning instance | Open `http://localhost:5680` |
| Key generator | Creates a console key, two automation keys, and two server keys in ignored local `state/` |

The SSH and n8n ports bind to your machine's loopback interface. Generated private keys stay on your machine and are excluded from Git and the Docker build context.

## New to Docker?

Follow the [setup guide](docs/install.md) for Windows with WSL, macOS, Ubuntu, Debian, and Fedora. It explains how to install Docker and Compose, Git, an SSH client, and the small optional tools used by the helper commands.

On a Mac, use the [step-by-step Mac walkthrough](docs/mac.md) from installation through the first n8n run.

Already have Docker? Check that these commands work before continuing:

```bash
docker version
docker compose version
ssh -V
```

## Quick start

Run these commands in a terminal. On Windows, use an Ubuntu WSL terminal with Docker Desktop's WSL integration enabled.

```bash
cd ~
git clone https://github.com/low-country-cyber/lccs-ssh-playground.git
cd lccs-ssh-playground
docker compose up -d
./lab doctor
```

The first startup downloads the n8n image and builds a small SSH image, so it may take a few minutes. The `key-init` service exits after generating keys; that is expected. `./lab doctor` checks both SSH identities and waits for n8n to become healthy.

### Step 1: connect from your terminal

```bash
./lab console
```

In the lab shell, try:

```sh
whoami
hostname
cat README.txt
```

Type `exit` when finished. The terminal helper uses a generated, pinned host key. It will refuse an unexpected SSH server identity.

To see the OpenSSH command behind `./lab console`, try [Challenge 02: Connect with OpenSSH](challenges/02-direct-ssh.md).

### Step 2: connect from n8n

You can complete the command line challenges first and return to all the n8n companions later.

1. Open [http://localhost:5680](http://localhost:5680) and create the owner account for this new lab instance.
2. Run `./lab setup-n8n` in your terminal, then refresh n8n. This imports both automation credentials and every bundled workflow without displaying private keys or needing an n8n API key.
3. Open **SSH Playground - First Contact** from the workflow list and execute it manually. Its output should show `automation` and the lab target's hostname.

All bundled workflows stay inactive until you choose to run them. The public [workflow files](workflows/) contain no private key or credential ID; `./lab setup-n8n` binds each lab credential during import. You can rerun setup after adding lessons: it skips existing workflows so your edits remain, and refreshes the lab credentials from the current local keys. The n8n container reaches both SSH targets on the Compose network; your terminal uses `127.0.0.1:2222` for the first target and jumps through it to the hidden target.

Prefer to create the credentials in the n8n UI yourself? Run `./lab credential-info` to see the exact fields and local paths to the automation private keys. Keep those keys out of chat, screenshots, and Git.

## Helpful commands

| Command | What it does |
| --- | --- |
| `./lab status` | Shows the lab containers |
| `./lab doctor` | Checks both SSH logins and n8n health |
| `./lab automation 'whoami && hostname'` | Runs a command with the automation identity |
| `./lab credential-info` | Shows both n8n SSH credential fields without printing secrets |
| `./lab setup-n8n` | Imports both SSH credentials and all bundled workflows after owner setup |
| `./lab jump-config` | Adds the hidden target to a project-local SSH config |
| `docker compose logs --tail=50 ssh-target` | Shows recent SSH server logs |
| `docker compose down` | Stops the lab while keeping keys and n8n data |

Running `docker compose up -d` again preserves all generated SSH key pairs. To start completely fresh, follow the [reset instructions](docs/troubleshooting.md#start-fresh); a reset removes lab accounts, workflows, credentials, and keys.

## More help

- [First Contact challenge](challenges/01-first-contact.md)
- [Connect with OpenSSH challenge](challenges/02-direct-ssh.md)
- [Who trusts whom? challenge](challenges/03-who-trusts-whom.md)
- [Name your connection challenge](challenges/04-name-your-connection.md)
- [Deliver a file challenge](challenges/05-deliver-a-file.md)
- [Reach a private web service challenge](challenges/06-reach-a-private-service.md)
- [Reach a hidden SSH target challenge](challenges/07-jump-to-a-hidden-target.md)
- [Reuse one SSH connection challenge](challenges/08-reuse-one-connection.md)
- [Reach two services with one SOCKS proxy challenge](challenges/09-one-proxy-two-services.md)
- [Share a host page with Alpine challenge](challenges/10-share-a-host-page.md)
- [Installation guide](docs/install.md)
- [Mac walkthrough](docs/mac.md)
- [Troubleshooting and reset](docs/troubleshooting.md)
- [Security boundaries](SECURITY.md)

This is a local training project. It does not change your host SSH server or connect to real infrastructure. The code and documentation are released under the [MIT license](LICENSE).
