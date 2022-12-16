# vm setup

## set up ssh connection

First we connet to the vm instances via ssh connections. Follow the following steps to set up ssh

1. [create ssh key](https://cloud.google.com/compute/docs/connect/create-ssh-keys) on your local environment

2. add the generated public key to the project metadata
   - copy the contents of the `.pub` file
   - follow the guide [here](https://cloud.google.com/compute/docs/connect/add-ssh-keys#add_ssh_keys_to_project_metadata)

3. create a config file in the .ssh directory
   ```bash
   touch ~/.ssh/config
   ```

4. paste the text below into the config file and edit accordingly
   ```bash
    Host kafka-vm
        HostName <External IP Address>
        User <username>
        IdentityFile <~/.ssh/private_keyfile>
        LocalForward 9092 localhost:9092

    Host spark-master-node
        HostName <External IP Address Of Master Node>
        User <username>
        IdentityFile <~/.ssh/private_keyfile>
        LocalForward 8081 localhost:8081

    Host airflow-vm
        HostName <External IP Address>
        User <username>
        IdentityFile <~/.ssh/private_keyfile>
        LocalForward 8080 localhost:8080
   ```

5. connect to the vms in separate terminal windows
   ```bash
    ssh  kafka-vm
   ```

   ```bash
    ssh spark-master-node
   ```

   ```bash
    ssh airflow-vm
   ```

## setup vms

1. clone git repo and change directory to kafka
    ```bash
    git clone https://github.com/topefolorunso/musicaly-project.git ~/musicaly-project
    ```
    The following set up only applies to the kafka and airflow vms. The spark vm is managed by GCP so the necessary installation has been handled upon provisioning.

2. install python (anaconda dist), docker and docker-compose in the vm
    ```bash
    bash ~/musicaly-project/vm_setup/vm_setup.sh && \
    exec newgrp docker
    ```