from chispa import assert_df_equality
from helpers import *

def test_aggregate(spark):
    input_df =spark.createDataFrame(
        [("UDP",10,100),("TCP",0,30),("UDP",10,50),("TCP",1,20)],
        ["protocol","failed_logins","packet_count"]
    )

    expected = spark.createDataFrame(
        [("UDP",20,150),("TCP",1,50)],
        ["protocol","total_failed_logins","total_packets"]
    )
    actual = aggregate(input_df)
    assert_df_equality(actual,expected,ignore_nullable=True)

def test_aggregate2(spark):
    input_df = spark.createDataFrame(
        [("PortScan","TCP",1,1000,1),("Normal","UDP",1,1000,1),("Normal","UDP",1,200,1)],
        ["attack_type","protocol","duration","src_bytes","dst_bytes"]
    )
    expected = spark.createDataFrame(
        [("Normal","UDP",1.0,1200,2),("PortScan","TCP",1.0,1000,1)],
        ["attack_type","protocol","average_duration","source_bytes","destination_bytes"]
    )
    actual = aggregate2(input_df)
    assert_df_equality(actual,expected,ignore_nullable=True,ignore_row_order=True)
