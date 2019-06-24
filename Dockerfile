FROM python:3.7-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /src

WORKDIR /src

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock /src/

RUN pipenv install --system --dev

COPY . /src/
