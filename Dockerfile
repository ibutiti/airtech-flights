FROM python:3.7-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /src

WORKDIR /src

COPY requirements.txt /src/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src/
