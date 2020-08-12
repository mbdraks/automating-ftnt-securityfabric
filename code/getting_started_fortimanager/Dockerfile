FROM ubuntu:19.10

RUN set -x && \
    \
    echo "==> Installing python3 and dependencies..."  && \
    apt update && \
    apt install python3-pip --yes && \
    \
    echo "==> Installing Ansible..."  && \
    pip3 install ansible && \
    \
    echo "==> Installing Ansible collections..."  && \
    ansible-galaxy collection install fortinet.fortimanager

WORKDIR /ansible
