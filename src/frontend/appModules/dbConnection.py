import psycopg2
import configparser
import os.path as path

filepath =  path.abspath(path.join(__file__ ,"../../../.."))+'/config.ini'
config = configparser.ConfigParser()
config.read(filepath)

user = config.get('db','user')
password = config.get('db','password')
hostIP = config.get('db','hostIP')
database = config.get('db','database')
port = config.get('db','port')

def conEstablisher():
    """This function establishes connection to Postgres Database server on AWS

    Returns:
        cursor: a cursor to the database 
    """
    conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=hostIP,
            port=port
        )

    return conn.cursor()