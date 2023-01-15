import os
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.operators.python import PythonOperator

from dag_helper_functions import convert_to_parquet, upload_to_gcs



AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')

URL = 'https://github.com/topefolorunso/musicalyproject/raw/main/airflow/dbt/seeds/songs.csv'
CSV_FILENAME = 'songs.csv'
PARQUET_FILENAME = CSV_FILENAME.replace('csv', 'parquet')

CSV_OUTFILE = f'{AIRFLOW_HOME}/{CSV_FILENAME}'
PARQUET_OUTFILE = f'{AIRFLOW_HOME}/{PARQUET_FILENAME}'
TABLE_NAME = 'songs'

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'musicaly_staging')

with DAG(
    dag_id = f'load_songs_dag',
    description = f'Execute only once to create songs table in bigquery',
    schedule_interval="@once", #At the 5th minute of every hour
    # start_date=datetime(2022,3,20),
    # end_date=datetime(2022,3,20),
    # catchup=True,
    tags=['musicaly']
) as dag:

    start_task = EmptyOperator()

    download_songs_file_task = BashOperator(
        task_id = "download_songs_file",
        bash_command = f"curl -sSLf {URL} > {CSV_OUTFILE}"
    )

    convert_to_parquet_task = PythonOperator(
        task_id = 'convert_to_parquet',
        python_callable = convert_to_parquet,
        op_kwargs = {
            'csv_file' : CSV_OUTFILE,
            'parquet_file' : PARQUET_OUTFILE
        }
    )

    upload_to_gcs_task = PythonOperator(
        task_id='upload_to_gcs',
        python_callable = upload_to_gcs,
        op_kwargs = {
            'file_path' : PARQUET_OUTFILE,
            'bucket_name' : GCP_GCS_BUCKET,
            'blob_name' : f'{TABLE_NAME}/{PARQUET_FILENAME}'
        }
    )

    remove_files_from_local_task=BashOperator(
        task_id='remove_files_from_local',
        bash_command=f'rm {CSV_OUTFILE} {PARQUET_OUTFILE}'
    )

    create_external_table_task = BigQueryCreateExternalTableOperator(
        task_id = f'create_external_table',
        table_resource = {
            'tableReference': {
                'projectId': GCP_PROJECT_ID,
                'datasetId': BIGQUERY_DATASET,
                'tableId': TABLE_NAME,
            },
            'externalDataConfiguration': {
                'sourceFormat': 'PARQUET',
                'sourceUris': [f'gs://{GCP_GCS_BUCKET}/{TABLE_NAME}/*.parquet'],
            },
        }
    )

    end_task = EmptyOperator()

    start_task >> download_songs_file_task >> convert_to_parquet_task >> upload_to_gcs_task >> \
        [remove_files_from_local_task, create_external_table_task] >> end_task
