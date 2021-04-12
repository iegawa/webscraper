from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 4, 9)
}

dag = DAG(dag_id='webscraper_dag', default_args=default_args, schedule_interval='0 * * * *', catchup=False)

t1 = BashOperator(
    task_id='schedule_webscraper_dag',
    bash_command="cd ~/CaseTecnico/webscraper && scrapy crawl book_exchange --logfile logfile", 
    dag=dag
)
