
from helpers import *
import pytest

def test_null_values(spark):
    df_cyber =df_init(spark)
    df_null = df_cyber.filter(col("protocol").isNull()).count()
    df_bytes = df_cyber.groupBy("attack_type", "protocol").agg(avg("duration").alias("average_duration"),
                                                               sum("src_bytes").alias("source_bytes"),
                                                               sum("dst_bytes").alias("destination_bytes")
                                                               )
    df_bytes_null = df_bytes.filter(col("average_duration").isNull()).count()

    assert df_null == 0
    assert df_bytes_null ==0


def test_valid_values(spark):
    df_cyber = df_init(spark)
    df_packet = df_cyber.groupBy("protocol").agg(sum("failed_logins").alias("total_failed_logins"),
                                                 (sum("packet_count").alias("total_packets")))

    df_packet_valid = df_packet.filter(~df_packet.protocol.isin(["UDP","TCP"])).count()

    assert df_packet_valid ==0
