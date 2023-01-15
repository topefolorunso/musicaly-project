# setup spark streaming

1. set the necessary environment variables
   ```bash
   export KAFKA_EXTERNAL_IP=<KAFKA.VM.EXTERNAL.IP>
   export GCS_BUCKET_NAME=<GCS BUCKET NAME>
   export GOOGLE_APPLICATION_CREDENTIALS="/home/tope/musicaly-project/gcp/google_credentials.json"
   ```
   Please note that you have to copy the service account credentials to the vm. Also, since the IP is ephemeral, you will have to repeat this every time you restart your VM or create a new shell session.

2. navigate to the spark directory and submit spark streaming job
   ```bash
   cd ~/musicaly-project/spark_streaming && \
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