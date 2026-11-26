#!/bin/sh
# Low Country Cyber Solutions SSH Playground
# Start the disposable SSH server after key-init has prepared its public keys.
set -eu

# The server receives authorized public keys from the read-only lab mount.
# Each account gets its own SSH directory and key, so the learner and n8n
# automation identities stay separate.
for lab_user in learner automation; do
  install -d -m 700 -o "$lab_user" -g "$lab_user" "/home/$lab_user/.ssh"
  install -m 600 -o "$lab_user" -g "$lab_user" \
    "/lab-server/${lab_user}_authorized_keys" "/home/$lab_user/.ssh/authorized_keys"
done

# Give first-time learners a harmless file to read after logging in.
printf '%s\n' 'LCCS SSH Playground: First Contact' \
  'This is a disposable lab target. No real infrastructure is connected.' \
  > /home/learner/README.txt
chown learner:learner /home/learner/README.txt

# This tiny web page is reachable only from the target's own loopback address.
# Challenge 06 opens a learner-only SSH tunnel to it; Docker publishes no web port.
busybox-extras httpd -p 127.0.0.1:8080 -h /srv/lab-http

# Stay in the foreground so Docker can supervise sshd and collect its logs.
exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config
