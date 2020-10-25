from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 10),
    'catch_up':False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'unbiased', default_args=default_args)

directory = 'src/dataingestion'
scraper = BashOperator(
    task_id = 'getUrls',
    bash_command = 'sh runScraper.sh' ,
    dag = dag
)

direcotry = 'src/decompressor'
decompressor = BashOperator(
    task_id ='fileDecompressor',
    bash_command = 'sh decompressor.sh',
    dag = dag
)

direcotry = 'src/processor'
wikiProcessor = BashOperator(
    task_id = 'wikiFileProcessor',
    bash_command = 'sh wiki_run.sh',
    dag = dag
)

gdeltProcessor = BashOperator(
    task_id = 'gdeltFileProcessor',
    bash_command = 'sh gdelt_run.sh',
    dag = dag
)

scraper >> decompressor >> wikiProcessor >> gdeltProcessor
