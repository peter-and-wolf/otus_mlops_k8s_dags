from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd

import settings


class Joke(BaseModel):
  joke_id: int  
  text: str
  rating: float


class JokeResponse(BaseModel):
  jokes: list[Joke]


app = FastAPI()
api_prefix = '/api/v1'
cfg = settings.Config()
df = pd.read_csv(
  cfg.jokes_csv_path
).reset_index().rename(
  columns={'index': 'joke_id'}
)	


def get_sample(df: pd.DataFrame) -> JokeResponse:
  return JokeResponse(
    jokes=[
      Joke(
        joke_id=s['joke_id'], 
        text=s['text'], 
        rating=s['rating']
      ) for _, s in df.sample(n=cfg.response_size).iterrows()
    ]
  )


@app.get(f'{api_prefix}/jokes')
def jokes() -> JokeResponse:
  return get_sample(df)