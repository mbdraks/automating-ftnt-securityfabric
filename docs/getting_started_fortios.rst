.. getting_started_fortios:

Getting Started - FortiOS
########################################################################

In this article, we will cover how to change two global parameters on a
FortiGate using Ansible.

.. contents::

Overview
************************************************************************

In this article were going to use docker to simplify the workflow and
isolate our local machine packages and libraries from the control node,
using a docker image will also make it easier for an administrator to
use this recipe as it will not depend on any specific OS from the host
machine.

After we have our docker container running we will install Ansible on
the control node (which can be your notebook or a server that has
connectivity to the FortiGate) and run a simple playbook.

Versions
************************************************************************

.. list-table::
   :header-rows: 1

   * - Software
     - Version
   * - FortiGate-VM 
     - 6.4.0
   * - Ansible
     - 2.9.11
   * - Python
     - 3.7.5
   * - fortinet.fortios collection
     - 1.0.10

`Last updated: 2020-08-12`

Recipe
************************************************************************

1. Install Docker and start a container
========================================================================

- Install docker using the `official instructions <https://docs.docker.com/get-docker/>`_
- After docker is installed, start a container:

.. code-block:: console

    $ docker pull ubuntu:19.10


Now it's interesting to create a new folder that will hold like the
playbook and inventory files.

.. code-block:: console

    $ mkdir ansible   # or the equivalent on your OS 
    $ cd ansible
    $ docker run \
        --name ansible \
        --interactive \
        --tty \
        --mount type=bind,source="$(pwd)",target=/ansible \
        ubuntu:19.10

This will start a container named `ansible` and mount the local folder
to the container folder `/ansible`, this will be useful because you
will edit the playbooks and other files at your machine and they will be
transparently available to the container at this folder.

2. Install Ansible
========================================================================

You should be at your container bash at this point, let's proceed and install ansible.

.. code-block:: console

    # apt update
    # apt install python3-pip
    # pip3 install ansible

    # ansible --version
    ansible 2.9.10
    config file = None
    configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
    ansible python module location = /usr/local/lib/python3.7/dist-packages/ansible
    executable location = /usr/local/bin/ansible
    python version = 3.7.5 (default, Apr 19 2020, 20:18:17) [GCC 9.2.1 20191008]


It's important to have ansible running with Python 3 interpreter or else
you may see some errors during playbook execution like:

.. code-block:: console

    An exception occurred during task execution. To see the full
    traceback, use -vvv. The error was:
    ansible.module_utils.connection.ConnectionError: addinfourl instance
    has no attribute 'getheaders'


3. Install FortiOS module collection from Ansible Galaxy
========================================================================

.. code-block:: console

    # ansible-galaxy collection install fortinet.fortios


4. Create inventory and playbook file
========================================================================

Now we will create a inventory file that will contain details of our
FortiGate and a simple playbook that will have the configuration steps
we want to automate.

.. code-block:: console

    # cd /ansible
    # touch hosts


At your machine open your favorite text editor and put the following
text on the `hosts` file that now should be at your ansible folder.

.. warning::

  It's best practice to create a specific user for this and handle
  it's password using `ansible vault
  <https://docs.ansible.com/ansible/latest/network/getting_started/first_inventory.html>`_
  but for simplicity we will not use this method now.

.. literalinclude:: ../code/getting_started_fortios/hosts
   :language: INI
   :caption: hosts

Now create a new file named `fw_global_set.yml`, this is our playbook.
Here's the content:

.. literalinclude:: ../code/getting_started_fortios/fw_global_set.yml
   :language: YAML
   :linenos:
   :caption: fw_global_set.yml


Let's explore each part of this file.

.. literalinclude:: ../code/getting_started_fortios/fw_global_set.yml
   :language: YAML
   :linenos:
   :lines: 3-6
   :lineno-start: 3

This section is showing us that the scope of this playbook (where the
tasks will run) is the `fortigates` group defined in our inventory file
(hosts). It's also using the collections fortinet.fortios so we don't
have to use the complete name of the modules on every task and finally
we configured it to use the httpapi, meaning that the connection will
use FortiOS REST API, not a SSH connection like is common with ansible.

.. literalinclude:: ../code/getting_started_fortios/fw_global_set.yml
   :language: YAML
   :linenos:
   :lines: 8-12
   :lineno-start: 8

These variables define the VDOM scope of our changes, the HTTPS port (in
this case the standard 443 port), and that we are not validating the
certs, you can change that if you're not using self-signed certificates
for the management access.


.. literalinclude:: ../code/getting_started_fortios/fw_global_set.yml
   :language: YAML
   :linenos:
   :lines: 14-20
   :lineno-start: 14

This is the specific task we are executing, using the module `fortios_system_global <https://galaxy.ansible.com/fortinet/fortios>`_
we are changing the `admintimeout` parameter to 60 and the `hostname` of
our FG to FG-ANSIBLE-TEST.


5. Execute the playbook
========================================================================

To run the playbook simply execute:

.. code-block:: console

    # ansible-playbook -i hosts fw_global_set.yml

    PLAY [fortigates] *****************************************************************************************************************************************************************************

    TASK [Gathering Facts] ************************************************************************************************************************************************************************
    ok: [fortigate01]

    TASK [Configure global attributes.] ***********************************************************************************************************************************************************
    [WARNING]: Ansible has detected version mismatch between FortOS system and galaxy, see more details by specifying option -vvv
    changed: [fortigate01]

    PLAY RECAP ************************************************************************************************************************************************************************************
    fortigate01                : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


In this example I'm running the playbook against a FortiGate on 6.4, the
standard collection version is to FortiGate 6.2 but in this particular
case there's no problem. If there's a syntax change on the API however
you may need to use the specific collection to your version, which are
listed on the `collection documentation <https://galaxy.ansible.com/fortinet/fortios>`_.

Now you have a working environment and can explore any other modules,
include more devices in your inventory and automate several pieces of
any deployment.
