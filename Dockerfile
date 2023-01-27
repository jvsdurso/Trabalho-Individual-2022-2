FROM python:3.8

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install