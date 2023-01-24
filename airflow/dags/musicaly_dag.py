import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

from schema import listen_events, auth_events, page_view_events
from task_templates import create_external_table, create_empty_table, insert_job, delete_external_table



EVENTS = ['listen_events', 'page_view_events', 'auth_events'] # we have data coming in from three events

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'musicaly_stg')

EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d%H") }}'

TABLE_MAP = { f"{event.upper()}_TABLE" : event for event in EVENTS}

MACRO_VARS = {
    "GCP_PROJECT_ID": GCP_PROJECT_ID, 
    "BIGQUERY_DATASET": BIGQUERY_DATASET, 
    "EXECUTION_DATETIME_STR": EXECUTION_DATETIME_STR
    }

MACRO_VARS.update(TABLE_MAP)

with DAG(
    dag_id = f'musicaly_dag',
    description = f'Hourly data pipeline to generate dims and facts for musicaly',
    schedule_interval="5 * * * *", #At the 5th minute of every hour
    start_date=datetime(2022,3,26,18),
    catchup=False,
    max_active_runs=1,
    user_defined_macros=MACRO_VARS,
    tags=['musicaly']
) as dag:
    
    start_task = EmptyOperator()
    
    initate_dbt_task = BashOperator(
        task_id = 'dbt_initiate',
        bash_command = 'cd /dbt && dbt deps && dbt seed --select state_codes --profiles-dir . --target prod'
    )

    execute_dbt_task = BashOperator(
        task_id = 'dbt_musicaly_run',
        bash_command = 'cd /dbt && dbt deps && dbt run --profiles-dir . --target prod'
    )

    end_task = EmptyOperator()

    for event in EVENTS:
        
        insert_query        = f"{{% include 'sql/{event}.sql' %}}" #extra {} for f-strings escape
        external_table_name = f'{event}_{EXECUTION_DATETIME_STR}'
        events_data_path    = f'{event}/month={EXECUTION_MONTH}/day={EXECUTION_DAY}/hour={EXECUTION_HOUR}'
        events_schema       = eval(event)

        create_external_table_task  = create_external_table(event, GCP_PROJECT_ID, BIGQUERY_DATASET, external_table_name, GCP_GCS_BUCKET, events_data_path)
        create_empty_table_task     = create_empty_table(event, GCP_PROJECT_ID, BIGQUERY_DATASET, event, events_schema)
        execute_insert_query_task   = insert_job(event, insert_query, BIGQUERY_DATASET, GCP_PROJECT_ID)
        delete_external_table_task  = delete_external_table(event, GCP_PROJECT_ID, BIGQUERY_DATASET, external_table_name)
        
        start_task >> create_external_table_task >> create_empty_table_task >> execute_insert_query_task >> delete_external_table_task >> \
        initate_dbt_task >> execute_dbt_task