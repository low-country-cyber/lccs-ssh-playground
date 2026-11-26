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
printf '%s\n' "LCCS SSH Playground: ${LAB_TARGET_LABEL:-First Contact}" \
  'This is a disposable lab target. No real infrastructure is connected.' \
  > /home/learner/README.txt
chown learner:learner /home/learner/README.txt

# Only the first target runs the private pages for Challenges 06 and 09.
# The hidden target stays a separate SSH endpoint with no web listener.
if [ "${LAB_WEB_SERVICE:-yes}" = yes ]; then
  busybox-extras httpd -p 127.0.0.1:8080 -h /srv/lab-http
  busybox-extras httpd -p 127.0.0.1:8081 -h /srv/lab-status
fi

# Stay in the foreground so Docker can supervise sshd and collect its logs.
exec /usr/sbin/sshd -D -e -f "${LAB_SSHD_CONFIG:-/etc/ssh/sshd_config}"
