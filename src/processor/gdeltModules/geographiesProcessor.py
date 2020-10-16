from functools import reduce
from pyspark.sql.functions import lower, col

def geographiesProcessor(dataframe):
    """This function processes mentions data from GDELT databases

    Args:
        dataframe (dataframe):  mentions data dataframe to be processed to generate keywords dataset

    Returns:
        dataframe: processed dataframe from raw data
    """
    
    df = dataframe

    dfCols = ['_c0','_c2','_c5','_c11','_c13']
    dfnewColumns = ['GLOBALEVENTID','MentionTimeDate','MentionIdentifier','Confidence','MentionDocTone']

    df = df.select("globaleventid","actor1name", "actor1geo_fullname","actor2name","actor2geo_fullname","actiongeo_fullname")\
            .withColumn('actor1name', lower(col('actor1name')))\
            .withColumn('actor1geo_fullname', lower(col('actor1geo_fullname')))\
            .withColumn('actor2name', lower(col('actor2name')))\
            .withColumn('actor2geo_fullname', lower(col('actor2geo_fullname')))\
            .withColumn('actiongeo_fullname', lower(col('actiongeo_fullname')))
            
    dfoldColumns = df.schema.names
    df = reduce(lambda data, idx: data.withColumnRenamed(dfoldColumns[idx],\
            dfnewColumns[idx].lower()), range(len(dfoldColumns)), df)
    df = df.select("globaleventid", "mentionidentifier", "confidence", "mentiondoctone",\
            to_timestamp(col("mentiontimedate"), "yyyyMMddHHmmss").alias('timestamp'))\
            .withColumn("globaleventid", col("globaleventid").cast('int'))\
            .withColumn("confidence", col("confidence").cast('int'))\
            .withColumn("mentiondoctone", col("mentiondoctone").cast('float'))\
            .select("globaleventid", "actor1name","actor1geo_fullname","actor2name","actor2geo_fullname","actiongeo_fullname")

    return df