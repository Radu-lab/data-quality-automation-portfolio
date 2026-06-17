from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pytest

def df_init(spark_init):
    df_cyber = spark_init.read.csv("cyber_attack_dataset_100000.csv"
                                   , header=True, inferSchema=True)
    return df_cyber

def aggregate(df):
    df_packet = df.groupBy("protocol").agg(sum("failed_logins").alias("total_failed_logins"),
                                                 (sum("packet_count").alias("total_packets")))
    return df_packet

def aggregate2(df):
    df_bytes = df.groupBy("attack_type", "protocol").agg(avg("duration").alias("average_duration"),
                                                               sum("src_bytes").alias("source_bytes"),
                                                               sum("dst_bytes").alias("destination_bytes")
                                                               )
    return df_bytes