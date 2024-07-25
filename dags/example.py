from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
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

  task2 = KubernetesPodOperator (
    task_id='joke-to-s3',
    name='joke-to-s3',
    image='peterwolf/joke-to-s3:latest',
    cmds = [
      'python', 'main.py', 
      '--joke-endpoint', 'http://51.250.39.188/api/v1/jokes',
      '--s3-endpoint', 'https://storage.yandexcloud.net',
      '--bucket', 'k8s-outliers',
      '--filekey', 'jokes/qwerty12345'
    ],
    secrets=[aws_access_key_id, aws_secret_access_key]
  )

task1 >> task2
