import csv
from typing import Any

import boto3 # type: ignore
import requests

jokeapi_endpoint = 'http://51.250.33.39:8000/api/v1/jokes'
tmp_jokes_path = 'jokes.tmp.csv'
bucket_name = 'k8s-outliers' 
bucket_key_name = 'jokes/qwerty12345'


def get_jokes(endpoint: str):
  return requests.get(endpoint).json()['jokes']


def save_to_local(path: str, endpoint: str):
  with open(path, 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow(['joke_id', 'text', 'rating'])
    for j in get_jokes(endpoint):
      writer.writerow([j['joke_id'], j['text'], j['rating']])


if __name__ == "__main__":
  session = boto3.session.Session()
  s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
  )  

  save_to_local(tmp_jokes_path, jokeapi_endpoint)

  s3.upload_file(tmp_jokes_path, bucket_name, bucket_key_name)

  
