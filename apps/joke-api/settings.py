from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import FilePath

class Config(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env')
  jokes_csv_path: FilePath = Path('data/jokes.csv')
  response_size: int = 10_000