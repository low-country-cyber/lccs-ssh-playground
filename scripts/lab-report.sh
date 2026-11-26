#!/bin/sh
# Low Country Cyber Solutions SSH Playground
# sshd runs this fixed, root-owned script when the report-only key logs in.
# Do not evaluate SSH_ORIGINAL_COMMAND: the point is that a client's requested
# shell or command cannot change what this key runs.
set -eu

printf '%s\n' 'LCCS SSH Playground: restricted report'
printf 'Account: %s\n' "$(id -un)"
printf 'Target: %s\n' "$(hostname)"
printf '%s\n' 'The requested SSH command was not run.'
