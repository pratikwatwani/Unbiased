from functools import reduce
import pyspark.sql.functions as F
from pyspark.sql.functions import col


def mentionsProcessor(dataframe):
    """This function processes mentions data from GDELT databases

    Args:
        dataframe (dataframe): raw mentions data dataframe to be processed

    Returns:
        dataframe: processed dataframe from raw data
    """
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
            .withColumn("mentiondoctone", col("mentiondoctone").cast('float'))\
            .select("globaleventid","confidence","mentiondoctone", "timestamp")

    return df