# Kafka VM Setup

1. establish [ssh connection](../vm_setup/README.md) to the KAFKA VM
2. clone git repo and change directory to kafka
    ```bash
    git clone https://github.com/topefolorunso/musicaly-project.git ~/musicaly-project && \
    cd ~/musicaly-project/kafka
    ```
3. install python (anaconda dist), docker and docker-compose in the vm
    ```bash
    bash ~/musicaly-project/vm_setup/vm_setup.sh && \
    exec newgrp docker
    ```
4. set the KAFKA external IP as an env variable
    ```bash
    export KAFKA_EXTERNAL_IP={KAFKA.VM.EXTERNAL.IP}
    ```
