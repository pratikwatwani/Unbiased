def metaProcessor(dataframe):
    df = dataframe
    df = df.withColumn("title", split(col("title"),' '))\
            .select("id", explode("title").alias('keyword'))\
            .groupBy('keyword')\
            .agg(collect_list('id').alias('id'))\

    df = {r.asDict()["keyword"]: r.asDict()["id"] for r in df.collect()}

    return df