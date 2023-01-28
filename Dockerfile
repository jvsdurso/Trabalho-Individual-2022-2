FROM python:3.8 AS python

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN python -m pip install --upgrade pip \
    pip install poetry

RUN poetry install

RUN apt update -y
RUN apt-get install python3-sphinx -y
RUN apt-get install doxygen sphinx-common -y

RUN doxygen doxygen.conf -y
RUN sphinx-build -b html docs/source docs/build

