FROM prefecthq/prefect:latest

WORKDIR /app

ADD imdb_rating .

RUN pip install scrapy pendulum sqlmodel