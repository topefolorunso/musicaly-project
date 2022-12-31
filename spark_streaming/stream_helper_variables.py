# Kafka Topics
import os


# kafka topics variables
LISTEN_EVENTS_TOPIC         = "listen_events"
PAGE_VIEW_EVENTS_TOPIC      = "page_view_events"
AUTH_EVENTS_TOPIC           = "auth_events"

# kafka bootstrap server address
KAFKA_PORT                  = "9092"
KAFKA_IP_ADDRESS            = os.getenv("KAFKA_EXTERNAL_IP", 'localhost')
KAFKA_BOOTSTRAP_SERVER      = f"{KAFKA_IP_ADDRESS}:{KAFKA_PORT}"

# google cloud storage bucket name and path
GCS_BUCKET_NAME             = os.getenv("GCS_BUCKET_NAME", 'musicaly-data-lake')
GCS_PATH                    = f'gs://{GCS_BUCKET_NAME}'

# path to files
LISTEN_EVENTS_PATH          = f"{GCS_PATH}/{LISTEN_EVENTS_TOPIC}"
PAGE_VIEW_EVENTS_PATH       = f"{GCS_PATH}/{PAGE_VIEW_EVENTS_TOPIC}"
AUTH_EVENTS_PATH            = f"{GCS_PATH}/{AUTH_EVENTS_TOPIC}"

# path to checkpoints
LISTEN_EVENTS_CHECKPOINT    = f"{GCS_PATH}/checkpoint/{LISTEN_EVENTS_TOPIC}"
PAGE_VIEW_EVENTS_CHECKPOINT = f"{GCS_PATH}/checkpoint/{PAGE_VIEW_EVENTS_TOPIC}"
AUTH_EVENTS_CHECKPOINT      = f"{GCS_PATH}/checkpoint/{AUTH_EVENTS_TOPIC}"