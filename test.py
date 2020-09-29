import sys
from operator import add
import configparser
import logging
import psycopg2
reload(sys)
sys.setdefaultencoding('UTF-8')

from pyspark.sql import SparkSession


if __name__ == "__main__":

    
    configFile = r'config.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)

    #host = str(config.get('DB','db_endpoint'))
    #dbname = str(config.get('DB','db'))
    #user = str(config.get('DB','db_user'))
    #password = str(config.get('DB','db_password'))
    #port = str(config.get('DB','db_port'))
    
    host = "ec2-18-206-170-90.compute-1.amazonaws.com"
    dbname = 't1'
    user = 'myuser'
    password = 'mypass'
    port = 5432

    print(host, dbname, user, password, port)
    logging.info('Establishing connection to the database')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(host, dbname, user, password, port))
    cur = conn.cursor()
    print(conn)

    spark = SparkSession\
        .builder\
        .appName("test")\
        .getOrCreate()
    """
    lines = spark.read.load(sys.argv[1], format="csv", sep="\t", inferSchema="true", header="false")
    lines = lines.select([c for c in lines.columns if c in ['_c0','_c1','_c60']])
    #output = lines.toPandas().to_csv('test.csv')
    print(lines.collect())
    """

    spark.stop()