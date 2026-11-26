# Run the SSH Playground on a Mac

This walkthrough uses macOS Terminal and Docker Desktop. The lab runs in containers; you do **not** need to turn on macOS **Remote Login** or change your Mac's SSH server.

The project has been tested end to end on Linux. These Mac steps follow the current official installation guides, but an end-to-end run on macOS has not yet been verified.

## 1. Install and start Docker Desktop

Download the version for your Mac's processor from Docker's [Mac installation guide](https://docs.docker.com/desktop/setup/install/mac-install/). Install and open Docker Desktop. Wait until it reports that the Docker engine is running.

Open **Terminal** and check both Docker and Compose:

```bash
docker version
docker compose version
```

`docker version` should show both a **Client** and a **Server**. If it cannot reach the server, open Docker Desktop and wait for startup to finish.

## 2. Check the small terminal tools

```bash
git --version
ssh -V
curl --version
python3 --version
```

Git, SSH, and curl are needed for the steps below. If Git is missing, the [Git macOS guide](https://git-scm.com/install/mac) includes the Xcode Command Line Tools option (`xcode-select --install`). Python 3 is needed for `./lab setup-n8n`, `./lab import-credential`, and Challenge 10's host page. If it is missing, use the [official Python macOS installer](https://www.python.org/downloads/macos/). You can create the n8n SSH credentials manually without Python, but Challenge 10 uses Python's built-in web server.

## 3. Download and start the lab

Run these commands in Terminal:

```bash
cd ~
git clone https://github.com/low-country-cyber/lccs-ssh-playground.git
cd lccs-ssh-playground
docker compose up -d
./lab doctor
```

Keep the repository in your home directory or another local folder where your user can own files. The first start downloads and builds images. The `key-init` container exiting successfully is expected. `./lab doctor` should show successful `learner` and `automation` logins and healthy n8n.

The lab uses only two Mac loopback ports: SSH on `127.0.0.1:2222` and n8n at `http://localhost:5680`. If either port is occupied, see [troubleshooting](troubleshooting.md#port-2222-or-5680-is-already-in-use).

## 4. Try SSH from Terminal

```bash
./lab console
```

Inside the lab shell, run:

```sh
whoami
hostname
cat README.txt
exit
```

This SSH session goes to the disposable container, not your Mac's SSH server.

## 5. Try the same task in n8n

1. Open [http://localhost:5680](http://localhost:5680) in your browser and create the lab's owner account.
2. Back in Terminal, from the repository directory, run `./lab setup-n8n`. Refresh the n8n page afterward.
3. Open **SSH Playground - First Contact** from the workflow list and execute it manually. It should return `automation` and the lab container hostname.

If you skipped Python 3, run `./lab credential-info` for the fields to enter in n8n **SSH Private Key** credentials, then import the desired JSON files from `workflows/` in the n8n editor. Open each imported SSH node and select the matching credential; the hidden target uses the second one listed by the helper. Read each key from its local file and paste it into the matching n8n credential. Keep private keys off GitHub and out of screenshots.

## Stop and return later

```bash
docker compose down
```

Your n8n account, workflows, credentials, and generated SSH keys remain for the next `docker compose up -d`. See [troubleshooting](troubleshooting.md) for permission, port, and reset issues.
