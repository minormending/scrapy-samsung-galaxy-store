FROM python:3.10

RUN mkdir /app
COPY pyproject.toml /app 
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


RUN mkdir /app/spiders
COPY spider_samsung_galaxy_store /app/spiders

ENTRYPOINT [ "scrapy", "crawl", "galaxy-store" ]