import uuid
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

aws_access_key_id = Secret('env', 'AWS_ACCESS_KEY_ID', 'ya-s3-secret', 'AWS_ACCESS_KEY_ID')
aws_secret_access_key = Secret('env', 'AWS_SECRET_ACCESS_KEY', 'ya-s3-secret', 'AWS_SECRET_ACCESS_KEY')


def hello_world(filekey: str):
  print(f'{datetime.now()}: {filekey} has uploaded to s3')


with DAG(dag_id="hello_world_dag",
         start_date=days_ago(2),
         schedule="*/5 * * * *",
         catchup=False) as dag:
  
  filekey = str(uuid.uuid4())

  task1 = KubernetesPodOperator (
    task_id='joke-to-s3',
    name='joke-to-s3',
    namespace='default',
    image='peterwolf/joke-to-s3:v1',
    cmds = [
      'python', 'main.py', 
      '--joke-endpoint', 'http://51.250.33.39:8000/api/v1/jokes',
      '--s3-endpoint', 'https://storage.yandexcloud.net',
      '--bucket', 'k8s-outliers',
      '--filekey', f'jokes/{filekey}'
    ],
    secrets=[aws_access_key_id, aws_secret_access_key],
    in_cluster=True
  )

  task2 = PythonOperator(
    task_id="hello_world",
    python_callable=hello_world,
    op_kwargs=dict(
      filekey=f'jokes/{filekey}'
    )
  )

task1 >> task2
