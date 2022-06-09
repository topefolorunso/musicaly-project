# musicaly-project

An end-to-end data pipeline that ingests simulated music stream data, structures, cleans and models the raw data, and visualizes clean data.

## Architecture

Eventsim -> Kafka -> Spark Streaming -> Google Cloud Storage -> BigQuery (staging) -> dbt -> BigQuery (production) -> Google Data Studio
