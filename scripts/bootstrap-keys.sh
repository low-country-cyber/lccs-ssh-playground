#!/bin/sh
# Low Country Cyber Solutions SSH Playground
# Compose runs this initializer before the SSH target. It creates the lab's
# client and server identities in the local, Git-ignored state directory.
set -eu
# New files start private, even before the explicit permissions below.
umask 077

mkdir -p /state/keys /state/server /state/hidden-server

# Keep existing identities across restarts. A half-written pair needs a human
# to inspect it; silently replacing it would also change who the lab trusts.
create_key() {
  key_path=$1
  key_label=$2
  if [ -e "$key_path" ] || [ -e "$key_path.pub" ]; then
    if [ ! -s "$key_path" ] || [ ! -s "$key_path.pub" ]; then
      echo "Incomplete key pair at $key_path; refusing to replace it" >&2
      exit 1
    fi
  else
    ssh-keygen -q -t ed25519 -N '' -C "$key_label" -f "$key_path"
  fi
  chmod 600 "$key_path"
  chmod 644 "$key_path.pub"
}

# The learner keeps one console identity across both targets. n8n gets a
# different automation identity for each target, and each server has its own
# host key. Only public client keys are copied to the server directories.
create_key /state/keys/console lccs-playground-console
create_key /state/keys/automation lccs-playground-automation
create_key /state/keys/hidden-automation lccs-playground-hidden-automation
create_key /state/server/ssh_host_ed25519_key lccs-playground-host
create_key /state/hidden-server/ssh_host_ed25519_key lccs-playground-hidden-host

# Only public client keys go into the server's authorized-keys files.
cat /state/keys/console.pub > /state/server/learner_authorized_keys
cat /state/keys/automation.pub > /state/server/automation_authorized_keys
cat /state/keys/console.pub > /state/hidden-server/learner_authorized_keys
cat /state/keys/hidden-automation.pub > /state/hidden-server/automation_authorized_keys
chmod 644 /state/server/*_authorized_keys /state/hidden-server/*_authorized_keys

# Pin this lab's server identity for ./lab console and ./lab automation.
# Those helpers reject an unexpected host key instead of accepting it blindly.
awk '{print "[127.0.0.1]:2222 " $1 " " $2}' \
  /state/server/ssh_host_ed25519_key.pub > /state/known_hosts
chmod 644 /state/known_hosts

# The hidden target has a separate pinned host key. HostKeyAlias in the
# project-local client config uses this stable name across the jump.
awk '{print "hidden-lab " $1 " " $2}' \
  /state/hidden-server/ssh_host_ed25519_key.pub > /state/hidden_known_hosts
chmod 644 /state/hidden_known_hosts

# The checked-in state directory is owned by the person who cloned the repo.
# Give that person access to the client keys without broadening key permissions.
state_owner=$(stat -c '%u:%g' /state)
chown "$state_owner" /state/keys /state/keys/console /state/keys/console.pub \
  /state/keys/automation /state/keys/automation.pub \
  /state/keys/hidden-automation /state/keys/hidden-automation.pub \
  /state/known_hosts /state/hidden_known_hosts
chown "$state_owner" /state/server /state/server/*
chown "$state_owner" /state/hidden-server /state/hidden-server/*
chmod 700 /state/keys
chmod 700 /state/server /state/hidden-server

echo 'Lab keys are ready; existing key pairs were preserved.'
