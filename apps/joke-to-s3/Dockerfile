FROM python:3.12-slim

WORKDIR /app

ENV LOG_LEVEL=DEBUG

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
