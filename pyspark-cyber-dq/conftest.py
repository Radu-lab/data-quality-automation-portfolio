from pyspark.sql import SparkSession
import sys
import os
import pytest

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

@pytest.fixture(scope = "session")
def spark():
    spark = SparkSession.builder.appName("cyberAttacks").master("local[*]").getOrCreate()
    yield spark