# Challenge 05: Deliver a file

![A learner sends a sealed file to the SSH lab server and retrieves a matching copy](../assets/challenge-05-file-transfer.png)

## Goal

Move a harmless file from your host to the Alpine lab with `scp`, retrieve it with `sftp`, and confirm the round trip did not change its contents. Both tools use the same SSH identity and host-key settings as your terminal connection.

## 1. Start from a fresh clone

In the playground directory, run:

```bash
docker compose up -d
./lab doctor
./lab ssh-config > state/ssh_config
chmod 600 state/ssh_config
```

The last two commands create the project-local `playground` alias from Challenge 04. They do not display or copy a private key.

## 2. Make a harmless local file

```bash
printf 'Low Country Cyber Solutions SSH Playground parcel\n' > state/parcel.txt
cat state/parcel.txt
```

You should see the single line you just wrote. The file is under Git-ignored `state/`, so this exercise does not add it to the public repository.

## 3. Send it with scp

```bash
scp -F state/ssh_config state/parcel.txt playground:parcel.txt
ssh -F state/ssh_config playground 'ls -l parcel.txt'
```

The `playground:` prefix means the destination is on the remote Alpine account. The file should appear in `learner`'s home directory. The `-F` option gives `scp` the same project-local connection settings you used with `ssh`.

## 4. Bring it back with sftp

Start an interactive transfer session:

```bash
sftp -F state/ssh_config playground
```

At the `sftp>` prompt, enter these commands one at a time:

```text
pwd
lpwd
ls parcel.txt
get parcel.txt state/parcel-returned.txt
bye
```

`pwd` shows the remote directory; `lpwd` shows your local playground directory. `get` saves a copy under your local `state/` directory. After `bye`, you are back at your usual shell prompt.

## 5. Compare the two local files

```bash
cmp state/parcel.txt state/parcel-returned.txt && echo 'Files match'
```

Expect `Files match`. If `cmp` reports a difference, inspect the two files and repeat the transfer. This comparison checks the actual file contents, not just the filenames.

## Explain what happened

- In `playground:parcel.txt`, which side of the connection holds the file?
- Why do `scp` and `sftp` work with the same `state/ssh_config` as `ssh`?
- What does `lpwd` tell you that `pwd` does not?

Keep real secrets and customer files out of this disposable lab. If a transfer fails, run `./lab doctor` and see [troubleshooting](../docs/troubleshooting.md).
