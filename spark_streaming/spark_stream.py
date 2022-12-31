import os

from schema import listen_events_schema, page_view_events_schema, auth_events_schema
from stream_helper_functions import *
from stream_helper_variables import *



# initialize a spark session
spark = get_spark_session('Eventsim Stream')
spark.streams.resetTerminated()

# read events stream
listen_events           = read_kafka_stream(spark, KAFKA_BOOTSTRAP_SERVER, LISTEN_EVENTS_TOPIC)
page_view_events        = read_kafka_stream(spark, KAFKA_BOOTSTRAP_SERVER, PAGE_VIEW_EVENTS_TOPIC)
auth_events             = read_kafka_stream(spark, KAFKA_BOOTSTRAP_SERVER, AUTH_EVENTS_TOPIC)

# process event streams
listen_events           = process_stream(listen_events, listen_events_schema, LISTEN_EVENTS_TOPIC)
page_view_events        = process_stream(page_view_events, page_view_events_schema, PAGE_VIEW_EVENTS_TOPIC)
auth_events             = process_stream(auth_events, auth_events_schema, AUTH_EVENTS_TOPIC)

# write event streams to file
listen_events_writer    = write_stream_data_to_parquet(listen_events, LISTEN_EVENTS_PATH, LISTEN_EVENTS_CHECKPOINT)
page_view_events_writer = write_stream_data_to_parquet(page_view_events, PAGE_VIEW_EVENTS_PATH, PAGE_VIEW_EVENTS_CHECKPOINT)
auth_events_writer      = write_stream_data_to_parquet(auth_events, AUTH_EVENTS_PATH, AUTH_EVENTS_CHECKPOINT)

# start streaming
listen_events_writer.start()
auth_events_writer.start()
page_view_events_writer.start()

spark.streams.awaitAnyTermination()
