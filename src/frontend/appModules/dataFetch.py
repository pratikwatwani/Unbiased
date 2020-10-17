import psycopg2
import pandas as pd

from dbConnection import conEstablisher

cur = conEstablisher()

scoreQuery = open('scoreQuery.sql','r').read()

articleQuery = open('articleQuery.sql','r').read()

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

