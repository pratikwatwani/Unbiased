import psycopg2
import pandas as pd


conn = psycopg2.connect(
            dbname='ebwe',
            user="admin",
            password="admin",
            host="ec2-3-210-212-233.compute-1.amazonaws.com",
            port='5321'
        )

cur = conn.cursor()

scoreQuery ='''select sum(nummentions), avg(avgtone) from eventsXgeog 
                where actor1geo_fullname = '{0}' 
                or actor2geo_fullname= '{0}' and 
                extract(year from dateadded)={1};
            '''

articleQuery='''select title, count from wiki 
                where title like concat('%', (select actor1name from (select 
                actor1name, nummentions from eventsxgeog where 
                actor1geo_fullname='{0}'   and 
                extract(year from dateadded) = {1} 
                union all
                select 
                actor1name, nummentions from eventsxgeog where 
                actor2geo_fullname = '{0}'  and 
                extract(year from dateadded) = {1} 
                order by nummentions desc limit 1)as stats),'%') 
                and year = {1} order by count desc limit 5
            '''

def dataFetch(country, year, code):
    """This function returns the result of the called query as a dataframe to the main application file

    Args:
        country (string): The name of the country to filter the query
        year (int): The year for which query is filtered
        code (bool): Boolean value that decides execution of specific query

    Returns:
        dataframe: a dataframe of fetched values 
    """
    country = str(country)
    year = int(year)

    if code==0:
        command = scoreQuery
    else:
        command = articleQuery
    cur.execute(command.format(country.lower(), year))

    rows=cur.fetchall()
    result = pd.DataFrame(rows)
    return result

