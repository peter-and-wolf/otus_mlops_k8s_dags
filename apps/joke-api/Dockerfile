FROM python:3.12-slim

WORKDIR /app

ENV JOKES_CSV_PATH=jokes.csv

COPY main.py .
COPY settings.py .
COPY requirements.txt .
COPY data/jokes.csv jokes.csv

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80"]
