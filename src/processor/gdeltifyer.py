import sys
from operator import add
from functools import reduce
import datetime

from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.serializers import MarshalSerializer, FramedSerializer

from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import lower, col
import pyspark.sql.functions as F
from pyspark.sql.functions import expr

import configparser
import os.path as path



def dbWriter(dataframe, table):

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


def converter(dataframe, columns, to_type):
    df = dataframe
    cols = columns
    to_type = to_type

    for col_name in cols:
        df = df.withColumn(col_name, col(col_name).cast(to_type))

    return df


def mentionsProcessor(dataframe):
    df = dataframe

    dfCols = ['_c0','_c2','_c5','_c11','_c13']
    dfnewColumns = ['GLOBALEVENTID','MentionTimeDate','MentionIdentifier','Confidence','MentionDocTone']

    df = df.select([c for c in df.columns if c in dfCols])
    dfoldColumns = df.schema.names
    df = reduce(lambda data, idx: data.withColumnRenamed(dfoldColumns[idx],\
            dfnewColumns[idx].lower()), range(len(dfoldColumns)), df)
    df = df.select("globaleventid", "mentionidentifier", "confidence", "mentiondoctone",\
            to_timestamp(col("mentiontimedate"), "yyyyMMddHHmmss").alias('timestamp'))\
            .withColumn("globaleventid", col("globaleventid").cast('int'))\
            .withColumn("confidence", col("confidence").cast('int'))\
            .withColumn("mentiondoctone", col("mentiondoctone").cast('float'))

    df = converter(df, ['globaleventid','confidence'],'int')
    df = converter(df, ['mentiondoctone'],'float')

    return df


def eventProcessor(dataframe):
    df = dataframe

    dfCols = ['_c0', '_c1','_c6','_c16','_c25','_c26','_c30','_c31','_c32'\
            ,'_c33','_c34','_c35','_c36','_c43','_c44','_c51','_c52','_c59','_c60']

    dfnewColumns = ['GLOBALEVENTID','SQLDATE','Actor1Name','Actor2Name','IsRootEvent',\
            'EventCode','GoldsteinScale','NumMentions','NumSources','NumArticles','AvgTone',\
            'Actor1Geo_Type','Actor1Geo_FullName','Actor2Geo_Type','Actor2Geo_FullName',\
            'ActionGeo_Type','ActionGeo_FullName','DATEADDED','SOURCEURL']

    df = df.select([c for c in df.columns if c in dfCols])
    dfoldColumns = df.schema.names
    df = reduce(lambda data, idx: data.withColumnRenamed(dfoldColumns[idx],\
            dfnewColumns[idx].lower()), range(len(dfoldColumns)), df)

    df = df.filter((F.col("actor1geo_type")==1)\
            & (F.col("actor2geo_type")==1)\
            & (F.col("actiongeo_type")==1))\
            .withColumn("sqldate", to_timestamp(col("sqldate"), "yyyyMMdd"))\
            .withColumn("dateadded", to_timestamp(col('dateadded'), 'yyyyMMddHHmmss'))\
            .select([c for c in df.columns if c not in {'actor1geo_type', 'actor2geo_type','actiongeo_type'}])\
            .withColumn("globaleventid", col("globaleventid").cast('int'))\

    df = converter(df, ["globaleventid", "goldsteinscale", "nummentions", "numsources", "numarticles"], 'int')
    df = converter(df, ["avgtone"],'float')

    return df

if __name__ == "__main__":

    spark = SparkSession.builder\
            .appName("GDELTifyer")\
            .config("serializer", FramedSerializer())\
            .getOrCreate()

    events = 's3a://gdelt-open-data/v2/events/*'
    
    eventsDF = spark.read.csv(events, sep='\t',header=False)
    mentionsDF = spark.read.csv(mentions, sep='\t',header=False)

    dbWriter(eventsDF.select("globaleventid", "goldsteinscale", "nummentions", "numsources", "numarticles",\
                "avgtone", "dateadded", "sourceurl"), 'events')

    dbWriter(geographiesDF.select("globaleventid", "actor1name","actor1geo_fullname","actor2name","actor2geo_fullname",\
                "actiongeo_fullname"), 'geographies')

    
    eventsDF = eventProcessor(eventsDF)
    geographiesDF = eventsDF.select("globaleventid","actor1name", "actor1geo_fullname","actor2name",\
            "actor2geo_fullname","actiongeo_fullname")\
            .where(*[c.lower() for c in df.columns])\
            .withColumn('actor1name', lower(col('actor1name')))\
            .withColumn('actor1geo_fullname', lower(col('actor1geo_fullname')))\
            .withColumn('actor2name', lower(col('actor2name')))\
            .withColumn('actor2geo_fullname', lower(col('actor2geo_fullname')))\
            .withColumn('actiongeo_fullname', lower(col('actiongeo_fullname')))

    eventsDF = eventsDF\
            .select([c for c in eventsDF.columns if c not in {"actor1name","actor1geo_fullname",\
            "actor2name","actor2geo_fullname","actiongeo_fullname"}])

 
    mentions = 's3a://gdelt-open-data/v2/mentions/*'
    mentionsDF = mentionsProcessor(mentionsDF)

    dbWriter(mentionsDF.select("globaleventid","mentionidentifier","confidence","mentiondoctone", "timestamp"), 'mentions')
    

    spark.stop()
~                  