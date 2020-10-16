import configparser
import os.path as path

from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.serializers import MarshalSerializer

from gdeltModules.mentionsProcessor import mentionsProcessor
from gdeltModules.eventsProcessor import eventProcessor
from gdeltModules.geographiesProcessor import geographiesProcessor
from dbWriter import dbWriter


if __name__ == "__main__":
    
    spark = SparkSession.builder\
            .appName("GDELTbreaker")\
            .config("serializer", MarshalSerializer())\
            .getOrCreate()

    filepath =  path.abspath(path.join(__file__ ,"../../.."))+'/config.ini'
    config = configparser.ConfigParser()
    config.read(filepath)

    events = config.get('S3','gdeltevents')
    mentions = config.get('S3','gdeltmentions')

    eventsDF = spark.read.csv(events, sep='\t',header=False)
    mentionsDF = spark.read.csv(mentions, sep='\t',header=False)
    
    eventsDF = eventProcessor(eventsDF)
    dbWriter(eventsDF,'events')

    geographiesDF = geographiesProcessor(eventsDF)
    dbWriter(geographiesDF,'geographies')

    mentionsDF = mentionsProcessor(mentionsDF)
    dbWriter(mentionsDF,'mentions')

    spark.stop()
               