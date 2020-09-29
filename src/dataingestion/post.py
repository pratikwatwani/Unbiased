import sys
from operator import add

from pyspark.sql import SparkSession

if __name__ == "__main__":


    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()
    #s3://gdelt-open-data/v2/events/20150812124500.export.csv
    lines = spark.read.option("sep", "\t").csv(sys.argv[-1])
    lines = lines.rdd.map(lambda r: (r[0], r[1])).toDF()
    lines.show()
    spark.stop()
