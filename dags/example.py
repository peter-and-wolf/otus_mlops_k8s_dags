from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def hello_world():
  print(f'Hello World: {datetime.now()}')

with DAG(dag_id="hello_world_dag",
         start_date=days_ago(2),
         schedule="* * * * *",
         catchup=False) as dag:
  
  task1 = PythonOperator(
    task_id="hello_world",
    python_callable=hello_world
  )

task1
