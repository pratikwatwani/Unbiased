from functools import reduce
import pyspark.sql.functions as F
from pyspark.sql.functions import col

from typeCaster import converter

def eventProcessor(dataframe):
        """This function processes event data file from GDELT database 

        Args:
            dataframe (dataframe): raw events data dataframe to be processed

        Returns:
            dataframe: processed dataframe from raw data
        """
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

        df = df.select("globaleventid", "goldsteinscale", "nummentions", "numsources", "numarticles",
            "avgtone", "dateadded")

        return df