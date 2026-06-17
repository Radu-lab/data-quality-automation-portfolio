import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder.appName("cyberAttacks").master("local[*]").getOrCreate()

df_cyber = spark.read.csv("D:/Radu/AI_Upskilling/Kaggel/cyber_attacks/cyber_attack_dataset_100000.csv"
                          ,header=True, inferSchema=True)

df_cyber.show()
df_cyber.printSchema()

df_type = df_cyber.groupBy("attack_type").agg(sum("duration").alias("attack duration"))
df_type.show()

df_protocol = df_cyber.groupBy("protocol").agg(sum("failed_logins").alias("total_failed_logins"))
df_protocol.show()

df_packet = df_cyber.groupBy("protocol").agg(sum("failed_logins").alias("total_failed_logins"),
             (sum("packet_count").alias("total_packets")))
df_packet.show()

df_bytes = df_cyber.groupBy("attack_type","protocol").agg(avg("duration").alias("average_duration"),
            sum("src_bytes").alias("source_bytes"),
            sum("dst_bytes").alias("destination_bytes")
            )

df_bytes.show()
spark.stop()