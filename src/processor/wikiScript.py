from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext

from pyspark.serializers import MarshalSerializer
from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.functions import *

import configparser
import os.path as path

from tableProcessor import tableProcessor
from metaProcessor import metaProcessor
from dbWriter import dbWriter


if __name__ == "__main__":

    spark = SparkSession.builder\
            .appName("Wikibreaker")\
            .config("serializer", MarshalSerializer())\
            .getOrCreate()

    filepath =  path.abspath(path.join(__file__ ,"../../.."))+'/config.ini'
    config = configparser.ConfigParser()
    config.read(filepath)

    data = config.get('S3','wikipedia')

    df = spark.read.format('com.databricks.spark.xml')\
            .options(rowTag='page')\
            .load(data)

    df = df.select("id","title", explode("revision"))\
            .select("id","title","col.timestamp")\
            .withColumn("timestamp", to_timestamp(col("timestamp")))\
            .filter((F.col('id').isNotNull()) & (F.col('timestamp').isNotNull()) & (F.col('title').isNotNull()))

    WikiDF = tableProcessor(df)\
                .select('id','title')\
                .dropDuplicates()

    EditsDF = tableProcessor(df)\
                .select('id','timestamp')

    dbWriter(EditsDF, 'wikiedits')
    dbWriter(WikiDF, 'wikipedia')

    spark.stop()
                