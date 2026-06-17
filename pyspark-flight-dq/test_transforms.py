from chispa import assert_df_equality
from helpers import aggregate

def test_aggregate(spark):
    input_df = spark.createDataFrame(
        [("A","CPF",1,100),("A","CPF",1,50)],
        ["ENTITY_NAME","TYPE_MODEL","MONTH_NUM","DIST_FLOWN_KM"])
    expected = spark.createDataFrame(
        [("A","CPF",1,150)],
        ["ENTITY_NAME","TYPE_MODEL","MONTH_NUM","total_flown"]
    )
    actual = aggregate(input_df)
    assert_df_equality(actual,expected,ignore_nullable=True)