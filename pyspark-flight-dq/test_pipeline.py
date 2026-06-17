
from pyspark.sql.functions import sum
from pyspark.sql.functions import col
from helpers import init_df, aggregate


def test_reconciliation(spark):

    df = init_df(spark)
    df_group = aggregate(df)
    total_flown = df_group.agg(sum("total_flown")).collect()[0][0]
    dist_flown = df.agg(sum("DIST_FLOWN_KM")).collect()[0][0]

    assert total_flown == dist_flown

def test_uniqueness(spark):
    df = init_df(spark)
    df_group = df.groupBy(df.ENTITY_NAME,df.TYPE_MODEL,df.ENTRY_DATE).count()
    duplicates = df_group.filter(col("count") > 1)
    dup_count = duplicates.count()
    assert dup_count==0

def test_not_null(spark):
    df = init_df(spark)
    df_null_models = df.filter(df.DIST_FLOWN_KM.isNull()).count()
    assert df_null_models==0