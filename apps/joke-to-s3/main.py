import os
from typing import Annotated

import typer

def main(joke_endpoint: Annotated[str, typer.Option()], 
         s3_endpoint: Annotated[str, typer.Option()],
         bucket: Annotated[str, typer.Option()],
         filekey: Annotated[str, typer.Option()]):
  print(joke_endpoint)
  print(s3_endpoint)
  print(bucket)
  print(filekey)
  print(os.environ.get('AWS_ACCESS_KEY_ID', 'Unknown access key id')) 
  print(os.environ.get('AWS_SECRET_ACCESS_KEY', 'Unknown access key')) 


if __name__ == '__main__':
  typer.run(main)