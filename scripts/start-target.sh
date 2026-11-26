#!/bin/sh
set -eu

for lab_user in learner automation; do
  install -d -m 700 -o "$lab_user" -g "$lab_user" "/home/$lab_user/.ssh"
  install -m 600 -o "$lab_user" -g "$lab_user" \
    "/lab-server/${lab_user}_authorized_keys" "/home/$lab_user/.ssh/authorized_keys"
done

printf '%s\n' 'LCCS SSH Playground: First Contact' \
  'This is a disposable lab target. No real infrastructure is connected.' \
  > /home/learner/README.txt
chown learner:learner /home/learner/README.txt

exec /usr/sbin/sshd -D -e -f /etc/ssh/sshd_config
