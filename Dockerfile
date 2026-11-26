FROM alpine:3.22

RUN apk add --no-cache openssh-server openssh-client \
    && adduser -D -h /home/learner -s /bin/sh learner \
    && adduser -D -h /home/automation -s /bin/sh automation \
    && for lab_user in learner automation; do \
         random_password=$(head -c 48 /dev/urandom | base64); \
         printf '%s:%s\n' "$lab_user" "$random_password" | chpasswd; \
       done

COPY sshd_config /etc/ssh/sshd_config
COPY scripts/bootstrap-keys.sh scripts/start-target.sh /usr/local/bin/
RUN chmod 755 /usr/local/bin/bootstrap-keys.sh /usr/local/bin/start-target.sh
