from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext

import configparser
import os.path as path

filepath =  path.abspath(path.join(__file__ ,"../../.."))+'/config.ini'
config = configparser.ConfigParser()
config.read(filepath)

user = config.get('db','user')
password = config.get('db','password')
hostIP = config.get('db','hostIP')
database = config.get('db','database')
driver = config.get('db','driver')
port = config.get('db','port')


def dbWriter(dataframe, table):
    df = dataframe
    dbtable = table

    properties = {
            "user": user,
            "password": password,
            "driver": driver,
            "batchsize": "1000000"
            }

    port = 
    url = "jdbc:postgresql://{0}:{1}/{2}".format(hostIP, port, database)

    df.write.jdbc(url=url, table=dbtable, mode='append', properties=properties)