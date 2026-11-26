# Troubleshooting

Start with `./lab status` and `./lab doctor` in the repository directory. The messages below cover common first-run problems.

## Git says it cannot create the work tree and the shell says "getwd: no such file or directory"

Your terminal may still be inside a previous playground clone that was deleted. Run `cd ~` to enter an existing directory, then retry the [Quick start](../README.md#quick-start). Run `cd lccs-ssh-playground` only after `git clone` succeeds.

## Docker command or Compose is missing

Follow the [installation guide](install.md). The project uses `docker compose` with a space, which requires the Compose plugin or Docker Desktop.

## Cannot connect to the Docker daemon

Start Docker Desktop, or start the Docker service on Linux. Check `docker version` again. On Linux, Docker's [post-install guide](https://docs.docker.com/engine/install/linux-postinstall/) explains access options.

## Port 2222 or 5680 is already in use

The lab publishes SSH on `127.0.0.1:2222` and n8n on `127.0.0.1:5680`. Stop the conflicting local application, then run `docker compose up -d` again. Do not change only the Compose port mapping: the lab helper and pinned host-key entry also use these ports.

## The key-init service says "Exited (0)"

That is expected. It runs once to create or verify the SSH keys. The SSH target and n8n should remain running.

## n8n says the credential is missing

Complete the owner setup at `http://localhost:5680`, run `./lab setup-n8n`, and refresh the browser. Bundled workflows are imported with **SSH Playground Automation** already selected. The public workflow files do not embed a secret or credential ID.

## SSH says "Permission denied (publickey)"

Run `./lab doctor`, then inspect `docker compose logs --tail=50 ssh-target`. The helper uses its own keys in `state/keys`; your usual `~/.ssh` keys are not used. Keep the whole project in a filesystem that supports owner-only permissions on private keys.

## SSH says the host key changed

Stop and inspect the lab before accepting a new host key. The key in `state/known_hosts` is generated from this lab's server key. A changed key can mean the lab was reset or that you reached a different service on the same port. Do not disable strict host-key checking to make the message disappear.

## Challenge 06 tunnel does not open

Keep the SSH command running in Terminal A while you use `curl` or a browser in Terminal B. If SSH reports that local port `18080` is in use, choose another unused local port in both the `-L` and `curl` commands. Check the target-side page with `ssh -F state/ssh_config playground 'wget -qO- http://127.0.0.1:8080/'`. The target address and port in `-L` must remain `127.0.0.1:8080`.

## Start fresh

This removes **only this playground's generated state and Compose volume**, including its n8n owner account, workflows, credentials, and all SSH key pairs. Review what you need to keep first. From the playground repository directory:

```bash
docker compose down -v
rm -rf state/keys state/server
rm -f state/known_hosts
docker compose up -d
```

Do not run the reset commands from another directory. Run `./lab doctor` after the new startup.
