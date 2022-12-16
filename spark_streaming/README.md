# setup spark streaming

1. navigate to the spark directory
   
   ```bash
   cd ~/musicaly-project/spark_streaming
   ```

2. set the necessary environment variables
   ```bash
   export KAFKA_ADDRESS=<KAFKA.VM.EXTERNAL.IP>
   export GCP_GCS_BUCKET=<GCS BUCKET NAME>
   ```

3. start spark streaming
   ```bash
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 stream_all_events.py
   ```