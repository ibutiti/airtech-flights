FROM python:3.7-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /src

WORKDIR /src

COPY Pipfile Pipfile.lock /src/

RUN pip install --no-cache-dir pipenv

RUN pipenv install --system

COPY . /src/
