from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.serializers import MarshalSerializer

from pyspark.sql.functions import lower, col
from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.functions import *
from pyspark.sql.functions import collect_list
from pyspark.sql.functions import split
from pyspark.sql.functions import collect_list

import configparser
import os.path as path


def tableProcessor(dataframe):
        """This function processes Wikipedia data to produce generic table 

        Args:
            dataframe (dataframe): Spark processed dataframe from raw wikipedia dataset

        Returns:
            dataframe: Processed dataframe
        """

        df = dataframe
        df = df.withColumn('title',lower(col('title')))\
            .where("title not like('%user talk:%')")\
            .dropDuplicates()

        return df

def metaProcessor(dataframe):
        """This function processes Wikipedia data to produce a metadata lookup table for pattern matching

        Args:
            dataframe (dataframe): Spark processed dataframe from raw wikipedia dataset

        Returns:
            dataframe: Processed dataframe
        """
        df = dataframe
        df = df.withColumn("title", split(col("title"),' '))\
            .select("id", explode("title").alias('keyword'))\
            .groupBy('keyword')\
            .agg(collect_list('id').alias('id'))\

        df = {r.asDict()["keyword"]: r.asDict()["id"] for r in df.collect()}
    
        return df

def dbWriter(dataframe, table):
        """This function writes the final processed dataframe to the destination database via JDBC 

        Args:
            dataframe (dataframe): Spark processed final dataframe
            table (string): Name of the table for data insertion
        """
        df = dataframe
        dbtable = table

        filepath =  path.abspath(path.join(__file__ ,"../../.."))+'/config.ini'
        config = configparser.ConfigParser()
        config.read(filepath)

        user = config.get('db','user')
        password = config.get('db','password')
        hostIP = config.get('db','hostIP')
        database = config.get('db','database')
        driver = config.get('db','driver')
        port = config.get('db','port')

        properties = {
            "user": user,
            "password": password,
            "driver": driver
        }

        url = "jdbc:postgresql://{0}:{1}/{2}".format(hostIP, port,database)

        df.write.jdbc(url=url, table=dbtable, mode='append', properties=properties)


if __name__ == "__main__":
        spark = SparkSession.builder\
            .appName("Wikibreaker")\
            .config("serializer", MarshalSerializer())\
            .getOrCreate()


        data = 's3a://wikiscrape/extracted/*'

        df = spark.read.format('com.databricks.spark.xml')\
            .options(rowTag='page')\
            .load(data)\
            .coalesce(1000)\
            .select("id","title", explode("revision"))\
            .select("id","title","col.timestamp")\
            .withColumn("timestamp", to_timestamp(col("timestamp")))\
            .filter((F.col('id').isNotNull()) & (F.col('timestamp').isNotNull()) & (F.col('title').isNotNull()))


        WikiDF = tableProcessor(df)\
                .select('id','title')\
                .dropDuplicates()
                
        dbWriter(WikiDF, 'wikipedia')

        EditsDF = tableProcessor(df)\
                .select('id','timestamp')
    
        dbWriter(EditsDF, 'wikiedits')

        metadata = WikiDF.select("id", "title")
        metadata = metaProcessor(metadata)

        spark.stop()
