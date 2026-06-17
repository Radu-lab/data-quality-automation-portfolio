from pyspark.sql.functions import sum


def init_df(spark):
    df = spark.read.csv("flight_data2026.csv", header=True, inferSchema=True)
    return df

def aggregate(df):
    return df.groupBy("ENTITY_NAME","TYPE_MODEL","MONTH_NUM").agg(
        sum("DIST_FLOWN_KM").alias("total_flown")
    )