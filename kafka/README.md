# Kafka VM Setup


1. start the kafka service
   - set the KAFKA external IP as an env variable
      
       ```bash
       export KAFKA_EXTERNAL_IP=<KAFKA.VM.EXTERNAL.IP>
       ```
       Please note that since the IP is ephemeral, you will have to repeat this every time you restart your VM or create a new shell session

   - Start Kafka

       ```bash
       cd ~/musicaly-project/kafka && \
       docker-compose build && \
       docker-compose up 
       ```

   - open up the port 9092 and confirm that it is running fine

2. start the evensim service
   - run in another terminal window
  
        ```bash
        bash ~/musicaly-project/eventsim/eventsim_startup.sh 
        ```
    - to follow the logs
        ```bash
        docker logs --follow million_events
        ```
