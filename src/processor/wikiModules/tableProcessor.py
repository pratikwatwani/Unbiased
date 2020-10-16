from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext

from pyspark.sql.functions import lower, col

def tableProcessor(dataframe):
    """This function processed dataframes into a common structure and eliminates certain rows on conditions

    Args:
        dataframe (dataframe): spark dataframe to be processed into common structure

    Returns:
        dataframe: new dataframe 
    """
    df = dataframe
    df = df.withColumn('title',lower(col('title')))\
            .where("title not like('%user talk:%')")\
            .dropDuplicates()

    return df