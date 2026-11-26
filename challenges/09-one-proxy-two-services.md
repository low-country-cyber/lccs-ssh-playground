# Challenge 09: Reach two services with one SOCKS proxy

![A learner reaches two private services through one glowing SSH proxy](../assets/challenge-09-socks-proxy.png)

## Goal

Use one local SOCKS proxy to visit two different private web pages inside the Alpine target. In Challenge 06, `-L` mapped one local port to one destination. Here, `-D` lets each client request choose a destination from the lab's allowed list.

## 1. Start the lab and proxy in Terminal A

From the playground directory in a fresh clone, run **this entire block**:

```bash
docker compose up -d
./lab doctor
./lab ssh-config > state/ssh_config
chmod 600 state/ssh_config
ssh -F state/ssh_config -o ExitOnForwardFailure=yes -N -D 127.0.0.1:11080 playground
```

The blank screen after the final command is expected; keep Terminal A open. The SOCKS proxy listens at `127.0.0.1:11080` on **your computer**. `-N` carries traffic without opening a remote shell. The two web pages listen only at `127.0.0.1:8080` and `127.0.0.1:8081` **inside Alpine**; Docker publishes neither page to your computer.

## 2. Visit both pages in Terminal B

Open another terminal in the playground directory and run:

```bash
curl --noproxy '' --socks5-hostname 127.0.0.1:11080 --max-time 5 -fsS http://127.0.0.1:8080/ | grep 'LCCS SSH Playground private service'
curl --noproxy '' --socks5-hostname 127.0.0.1:11080 --max-time 5 -fsS http://127.0.0.1:8081/ | grep 'LCCS SSH Playground status service'
```

Expect one line naming each service. Both requests enter the **same** local SOCKS port, but ask for different destination ports. In these URLs, `127.0.0.1` means the Alpine target from the proxy's point of view. `--noproxy ''` keeps a local proxy-bypass setting from skipping this exercise; `--socks5-hostname` sends the destination through the SOCKS proxy.

The target's SSH server permits forwarding only to these two practice pages and the hidden SSH target from Challenge 07. This proxy is not a general route to other sites or ports.

## 3. Close the proxy

Return to Terminal A and press **Ctrl+C**. In Terminal B, verify the local proxy has stopped:

```bash
curl --noproxy '' --socks5-hostname 127.0.0.1:11080 --max-time 2 -fsS http://127.0.0.1:8080/ || echo 'SOCKS proxy is closed.'
```

The page still runs inside Alpine; only your host-side route is gone.

## n8n companion

After creating the n8n owner account, run `./lab setup-n8n` and refresh n8n. Open **SSH Playground - 09 - Two Private Services** and execute it manually. Its two SSH nodes read the two private pages as `automation` and show a line from each page.

n8n connects to the Alpine target with the saved **SSH Playground Automation** credential and runs `wget` there. It does not use your host-terminal SOCKS proxy, so you can run the workflow after closing Terminal A's tunnel.

## Explain what happened

- Which machine owns port `11080`, and which owns ports `8080` and `8081`?
- Why did one `-D` command work for both pages?
- Why can the n8n workflow read both pages after you close the host proxy?

If port `11080` is busy, choose another free local port in the SSH and `curl` commands. If a request fails, run `./lab doctor` and see the [troubleshooting guide](../docs/troubleshooting.md). Keep generated keys in `state/` out of screenshots and Git.
