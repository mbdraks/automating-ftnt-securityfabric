FROM ubuntu:19.10

RUN set -x && \
    \
    echo "==> Installing python3 and dependencies..."  && \
    apt update && \
    apt install python3-pip --yes && \
    \
    echo "==> Installing Ansible..."  && \
    pip3 install wheel setuptools && \
    pip3 install pywinrm && \
    pip3 install ansible && \
    \
    echo "==> Installing Ansible collections..."  && \
    echo "==> specific for FortiOS 6.2..."  && \
    ansible-galaxy collection install fortinet.fortios:1.0.10 && \
    ansible-galaxy collection install fortinet.fortimanager && \
    \
    echo "==> Installing generic fortios module"  && \
    mkdir -p /root/.ansible/plugins/modules/network/fortios && \
    mkdir -p /root/.ansible/plugins/module_utils/network/fortios

ADD https://raw.githubusercontent.com/fortinet/ansible-fortios-generic/master/fortios_json_generic.py /root/.ansible/plugins/modules/network/fortios
ADD https://raw.githubusercontent.com/fortinet/ansible-fortios-generic/master/fortios.py /root/.ansible/plugins/module_utils/network/fortios
ADD https://raw.githubusercontent.com/fortinet/ansible-fortimanager-generic/master/fmgr_generic.py /root/.ansible/plugins/modules/network/fortimanager

WORKDIR /ansible
