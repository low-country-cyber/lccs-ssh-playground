# Install the tools

This guide gets a new learner from a fresh machine to a working `docker compose` command. Use the section for your operating system, then run the checks at the end.

The end-to-end lab has been tested on Linux. The Windows WSL and macOS sections use the official installation paths but have not yet had an end-to-end playground run.

## What you need

| Tool | Needed for | Notes |
| --- | --- | --- |
| Docker Engine or Docker Desktop **with Compose** | Starting the lab | Use the modern `docker compose` command |
| Git | Cloning the repository | A GitHub ZIP download also works, but Git makes updates easier |
| OpenSSH client | `./lab console` and `./lab doctor` | The lab server runs inside Docker |
| curl | `./lab doctor` health check | Usually present on macOS; install on Linux if absent |
| Python 3 | `./lab import-credential` only | You can set the SSH credential manually without Python |

### Windows: Docker Desktop + Ubuntu WSL

1. Follow Docker's [Windows installation guide](https://docs.docker.com/desktop/setup/install/windows-install/) to install Docker Desktop with the WSL 2 backend.
2. Enable Docker Desktop's [WSL integration](https://docs.docker.com/desktop/features/wsl/) for your Ubuntu distribution. Start Docker Desktop.
3. Open an **Ubuntu WSL terminal**. Install the small terminal tools there:

   ```bash
   sudo apt update
   sudo apt install -y git openssh-client curl python3
   ```

4. Clone the repository inside your WSL home directory, such as `~/lccs-ssh-playground`. Keeping it on the Linux filesystem makes SSH key permissions more predictable than a Windows-mounted path.

Use the Quick start commands from the [README](../README.md#quick-start) in that same Ubuntu terminal. Docker Desktop supplies Docker and Compose to the integrated WSL distribution; do not install a second Docker daemon inside WSL.

### macOS: Docker Desktop

Follow the dedicated [Mac walkthrough](mac.md). It covers Docker Desktop installation, tool checks, cloning, the first terminal SSH session, the n8n credential, and stopping the lab.

### Ubuntu or Debian: Docker Engine + Compose plugin

1. Install Docker Engine using Docker's guide for [Ubuntu](https://docs.docker.com/engine/install/ubuntu/) or [Debian](https://docs.docker.com/engine/install/debian/). Follow its repository setup and package installation steps, including `docker-compose-plugin`. The [Compose plugin guide](https://docs.docker.com/compose/install/linux/) covers installing the plugin separately if Engine is already installed.
2. Install the terminal tools:

   ```bash
   sudo apt update
   sudo apt install -y git openssh-client curl python3
   ```

3. Make sure your user can run `docker compose version` and `docker compose ps`. If Docker reports a daemon permission error, use Docker's [Linux post-install guide](https://docs.docker.com/engine/install/linux-postinstall/) to choose an access method. Membership in the `docker` group gives broad control of the host, so use it only if appropriate for your machine.

Then follow the [Quick start](../README.md#quick-start).

### Fedora: Docker Engine + Compose plugin

1. Follow Docker's [Fedora installation guide](https://docs.docker.com/engine/install/fedora/), including the Compose plugin package. Start the Docker service as directed there.
2. Install the terminal tools:

   ```bash
   sudo dnf install -y git openssh-clients curl python3
   ```

3. Check Docker access using the [Linux post-install guide](https://docs.docker.com/engine/install/linux-postinstall/) if needed.

Then follow the [Quick start](../README.md#quick-start).

## Verify your installation

Run these in the same terminal you will use for the playground:

```bash
docker version
docker compose version
git --version
ssh -V
curl --version
python3 --version
```

The last command is optional if you plan to create the n8n credential manually. `docker version` should show both client and server information. If it reports that it cannot connect to the daemon, start Docker Desktop or the Linux Docker service before continuing.

The lab uses local ports `2222` and `5680`. Check that other applications are not using those ports before starting it. See [troubleshooting](troubleshooting.md) if startup reports an address conflict.
