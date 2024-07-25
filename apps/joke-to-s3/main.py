import os
import csv
import boto3 # type: ignore
import logging
from typing import Annotated

import requests
import typer


logging.getLogger().setLevel(
  level=os.environ.get('LOG_LEVEL', 'INFO').upper()
)


def get_jokes(endpoint: str):
  return requests.get(endpoint).json()['jokes']


def save_to_local(path: str, endpoint: str):
  with open(path, 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow(['joke_id', 'text', 'rating'])
    for j in get_jokes(endpoint):
      writer.writerow([j['joke_id'], j['text'], j['rating']])


def main(joke_endpoint: Annotated[str, typer.Option()], 
         s3_endpoint: Annotated[str, typer.Option()],
         bucket: Annotated[str, typer.Option()],
         filekey: Annotated[str, typer.Option()]):
  
  logging.debug(f'joke_endpoint={joke_endpoint}')
  logging.debug(f's3_endpoint={s3_endpoint}')
  logging.debug(f'bucket={bucket}')
  logging.debug(f'filekey={filekey}')

  # NEVER DO IN IRL
  # be attention trying not to miss that kind of 
  # things or better use secure code tools like bandit
  logging.debug(f"AWS_ACCESS_KEY_ID={os.environ.get('AWS_ACCESS_KEY_ID', 'Unknown access key id')}") 
  logging.debug(f"AWS_SECRET_ACCESS_KEY={os.environ.get('AWS_SECRET_ACCESS_KEY', 'Unknown access key')}") 

  session = boto3.session.Session()
  s3 = session.client(
    service_name='s3',
    endpoint_url=s3_endpoint
  )  

  local_path = '/tmp/jokes.csv'
  save_to_local(local_path, joke_endpoint)
  s3.upload_file(local_path, bucket, f'jokes/{filekey}')


if __name__ == '__main__':
  typer.run(main)