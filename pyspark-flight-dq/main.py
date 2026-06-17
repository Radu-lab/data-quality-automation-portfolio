import sys
import os
from pyspark.sql.functions import sum
from pyspark.sql.functions import col


os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("flight").master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("flight_data2026.csv", header=True,inferSchema=True)

df.show()
df.printSchema()

df_select = df.select("ENTITY_NAME","TYPE_MODEL","DIST_FLOWN_KM","DIST_DIRECT_KM","DIST_ACHIEVED_KM")
df_select.show()

df_filter = df.filter(df.TYPE_MODEL =='CPF')
df_filter.show()

df_group = df.groupBy(df.ENTITY_NAME,df.TYPE_MODEL,df.MONTH_NUM).agg(
            sum(df.DIST_FLOWN_KM).alias("total_flown"),
            sum(df.DIST_DIRECT_KM).alias("total_direct"),
            sum(df.DIST_ACHIEVED_KM).alias("total_achieved")
            )
df_eff = df_group.withColumn("efficiency",df_group.total_direct / df_group.total_flown)
df_eff.orderBy(df_eff.efficiency.desc()).show()

models = spark.createDataFrame(
    [("CPF", "actual flown"),
     ("FTFM", "filed plan")],
    #("SFR", "shortest route")],
    ["TYPE_MODEL", "description"]
)

df_models = df_group.join(models,"TYPE_MODEL","left")
df_models.show()
df_null_models = df_models.filter(df_models.description.isNull())
null_count = df_null_models.count()
if null_count>0:
    print(f"There are {null_count} rows !!!!")
    df_null_models.show()
else:
    print("All good no null values")

duplicates = df_group.groupBy("ENTITY_NAME","TYPE_MODEL","MONTH_NUM").count().filter(col("count")>1)
dup_count = duplicates.count()
if dup_count>0:
    print(f"ATENTIE: {dup_count} chei duplicate")
    duplicates.show()
else:
    print("OK, cheie unica")

total_flown = df_group.agg(sum("total_flown")).collect()[0][0]
#total_flown.collect()[0])
dist_flown = df.agg(sum("DIST_FLOWN_KM")).collect()[0][0]
if total_flown == dist_flown:
    print(f"Reconciliation succeded:{dist_flown} = {total_flown}")
else:
    print(f"Reconciliation failed:{dist_flown} != {total_flown}")
spark.stop()