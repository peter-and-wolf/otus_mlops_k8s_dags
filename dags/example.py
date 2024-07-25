from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.secret import Secret
from airflow.utils.dates import days_ago


aws_access_key_id = Secret('env', 'AWS_ACCESS_KEY_ID', 'ya-s3-secret', 'AWS_ACCESS_KEY_ID')
aws_secret_access_key = Secret('env', 'AWS_SECRET_ACCESS_KEY', 'ya-s3-secret', 'AWS_SECRET_ACCESS_KEY')

def hello_world():
  print(aws_access_key_id)
  print(aws_secret_access_key)
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
