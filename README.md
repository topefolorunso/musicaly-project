# musicaly-project

An end-to-end data pipeline that ingests simulated music stream data, structures, cleans and models the raw data, and visualizes clean data.

## Architecture

Eventsim -> Kafka -> Spark Streaming -> Google Cloud Storage -> BigQuery (staging) -> dbt -> BigQuery (production) -> Google Data Studio

## Data Source

## Dashboard

Click [here](https://datastudio.google.com/embed/reporting/1085eb37-b359-4613-90e2-71e54a82ff87/page/vYvuC) to view latest version on Data Studio

![](https://github.com/topefolorunso/musicaly-project/blob/main/Dashboard.png)
