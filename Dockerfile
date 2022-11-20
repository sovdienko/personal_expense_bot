FROM python:3.11

WORKDIR /home
ENV TELEGRAM_API_TOKEN=""
ENV TELEGRAM_ACCESS_ID=""

RUN pip install -U pip aiogram && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY *.sql ./
RUN sqlite3 finance.db < createdb.sql

ENTRYPOINT ["python", "server.py"]