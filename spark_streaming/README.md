# setup spark streaming

1. navigate to the spark directory
   
   ```bash
   cd ~/musicaly-project/spark_streaming
   ```

2. set the necessary environment variables
   ```bash
   export KAFKA_EXTERNAL_IP=<KAFKA.VM.EXTERNAL.IP>
   export GCS_BUCKET_NAME=<GCS BUCKET NAME>
   ```
   Please note that since the IP is ephemeral, you will have to repeat this every time you restart your VM or create a new shell session

3. start spark streaming
   ```bash
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 spark_stream.py
   ```

## how it works

spark executes this job in 3 basic steps

1. it reads the stream data from the kafka broker port 9092
2. it carries out data transformation on the stream data which includes:
   - schema specification
   - datetime transformation and
   - string encoding
3. then, every 120 seconds, it writes the transformed stream data in parquet format to specified GCS bucket and path.