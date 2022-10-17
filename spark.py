import os
from pyspark.sql import SparkSession
from app import main

os.environ['PYSPARK_PYTHON'] = "./pyspark_env/bin/python"
spark = SparkSession.builder.config(
    "spark.archives",  # 'spark.yarn.dist.archives' in YARN.
    "pyspark_venv.tar.gz#environment").getOrCreate()
main(spark)