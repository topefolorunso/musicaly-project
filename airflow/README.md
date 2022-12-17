# setup airflow

1. Copy the GCP service account credentials file to the VM using [sftp](https://youtu.be/ae-CV2KfoN0?t=2442)
   
2. set the necessary environment variables
   
   ```bash
   export GCP_PROJECT_ID=<project-id>
   export GCP_GCS_BUCKET=<GCS BUCKET NAME>
   ```
   Please note that you will have to repeat this every time you create a new shell session

3. start airflow service
   ```bash
   cd ~/musicaly-project/airflow && bash airflow_startup.sh
   ```
   the airflow UI should be available on port 8080. Proceed to login with default username and password of airflow

4. start the DAGs
   - trigger the `load_songs_dag` DAG first. This DAG is expected to run just once
   - trigger the `musicaly_dag` next. this DAG runs every hour on the 5th minute as thus;
     - We first create an external table for the data that was received in the past hour.
     - We then create an empty table to which our hourly data will be appended. Usually, this will only ever run in the first run.
     - Then we insert or append the hourly data, into the table.
     - And then, delete the external table.
     - Finally, run the dbt transformation, to create our dimensions and facts.

5. since airflow will be run in detached mode, run the commands below as needed
   ```bash
   <!-- to view the logs -->
   docker-compose --follow

   <!-- to stop airflow -->
   docker-compose down
   ```