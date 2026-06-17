
from helpers import *
import pytest

def test_null_values(spark):
    df_cyber =df_init(spark)
    df_null = df_cyber.filter(col("protocol").isNull()).count()
    df_bytes = aggregate2(df_cyber)
    df_bytes_null = df_bytes.filter(col("average_duration").isNull()).count()

    assert df_null == 0
    assert df_bytes_null ==0


def test_valid_values(spark):
    df_cyber = df_init(spark)
    df_packet = aggregate(df_cyber)

    df_packet_valid = df_packet.filter(~df_packet.protocol.isin(["UDP","TCP"])).count()

    assert df_packet_valid ==0
