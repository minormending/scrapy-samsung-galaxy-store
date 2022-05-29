FROM python:3.10

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir /app
COPY pyproject.toml /app
COPY README.md /app
COPY scrapy.cfg /app

RUN mkdir -p /app/spider_samsung_galaxy_store
COPY spider_samsung_galaxy_store /app/spider_samsung_galaxy_store

WORKDIR /app
RUN poetry install --no-dev

ENTRYPOINT [ "scrapy", "crawl", "galaxy-store" ]