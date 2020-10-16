from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql.functions import col

def converter(dataframe, columns, to_type):
    """This is a utility function to convert column types of dataframe

    Args:
        dataframe (dataframe): dataframe to be referred to for which conversion needs to be done
        columns (list): list of all column names to be recasted
        to_type (str): data type to convert the column to

    Returns:
        dataframe: returns a new dataframe with recasted selected columns
    """
    df = dataframe
    cols = columns
    to_type = to_type

    for col_name in cols:
        df = df.withColumn(col_name, col(col_name).cast(to_type))

    return df