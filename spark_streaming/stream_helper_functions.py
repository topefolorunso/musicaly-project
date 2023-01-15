from pyspark.sql import SparkSession

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import from_json, col, month, hour, dayofmonth, col, year, udf
from pyspark.sql.streaming import DataStreamWriter
from pyspark.sql.types import StructType



def get_spark_session(app_name: str, master: str="yarn") -> SparkSession:
    """
    Creates or gets a Spark Session

    Parameters:
        app_name : str
            Pass the name of your app
        master : str
            Choosing the Spark master, yarn is the default
    Returns:
        spark: SparkSession
    """
    
    spark = SparkSession.builder.appName(app_name).master(master=master).getOrCreate()
    return spark

@udf
def string_decode(string: str, encoding: str='utf-8') -> str:
    if string:
        return (string.encode('latin1')  # To bytes, required by 'unicode-escape'
            .decode('unicode-escape')    # Perform the actual octal-escaping decode
            .encode('latin1')            # 1:1 mapping back to bytes
            .decode(encoding)            # Decode original encoding
            .strip('\"'))
    else:
        return string

def read_kafka_stream(spark_session: SparkSession, kafka_bootstrap_server: str, topic: str, starting_offset:str ="earliest") -> DataFrame:
    """
    Creates a kafka read stream

    Parameters:
        spark : SparkSession
            A SparkSession object
        kafka_bootstrap_server: str
            server address of the kafka bootstrap server
        topic : str
            Name of the kafka topic
        starting_offset: str
            Starting offset configuration, "earliest" by default 
    Returns:
        read_stream: DataStreamReader
    """

    read_stream = spark_session \
                   .readStream \
                   .format("kafka") \
                   .option("kafka.bootstrap.servers", kafka_bootstrap_server) \
                   .option("failOnDataLoss", False) \
                   .option("startingOffsets", starting_offset) \
                   .option("subscribe", topic) \
                   .load()

    return read_stream

def process_stream(stream_df: DataFrame, stream_schema: StructType, topic: str) -> DataFrame:
    """
    Process stream to fetch on value from the kafka message.
    convert ts to timestamp format and produce year, month, day,
    hour columns
    Parameters:
        stream : DataStreamReader
            The data stream reader for your stream
    Returns:
        stream: DataStreamReader
    """

    # read only value from the incoming message and convert the contents
    # inside to the passed schema
    stream_df = stream_df \
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), stream_schema).alias("data")) \
        .select("data.*")

    # Add month, day, hour to split the data into separate directories
    stream_df = stream_df \
        .withColumn("ts", (col("ts")/1000).cast("timestamp")) \
        .withColumn("year", year(col("ts"))) \
        .withColumn("month", month(col("ts"))) \
        .withColumn("day", dayofmonth(col("ts"))) \
        .withColumn("hour", hour(col("ts")))

    # rectify string encoding
    if topic != "auth_events":
        stream_df = stream_df \
            .withColumn("song", string_decode("song")) \
            .withColumn("artist", string_decode("artist")) 
                
    return stream_df

def write_stream_data_to_parquet(stream_df: DataFrame, storage_path: str, checkpoint_path: str, trigger: str="120 seconds", output_mode: str="append", file_format: str="parquet") -> DataStreamWriter:
    """
    Write the stream back to a file store

    Parameters:
        stream : DataStreamReader
            The data stream reader for your stream
        file_format : str
            parquet, csv, orc etc
        storage_path : str
            The file output path
        checkpoint_path : str
            The checkpoint location for spark
        trigger : str
            The trigger interval
        output_mode : str
            append, complete, update
    """

    stream_writer = stream_df \
                    .writeStream \
                    .format(file_format) \
                    .partitionBy("month", "day", "hour") \
                    .option("path", storage_path) \
                    .option("checkpointLocation", checkpoint_path) \
                    .trigger(processingTime=trigger) \
                    .outputMode(output_mode)

    return stream_writer