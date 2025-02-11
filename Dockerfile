FROM python:3.11-alpine

RUN mkdir /app

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev
RUN pip install -U pip setuptools wheel ruamel.yaml.clib

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Goutom Roy" version="1.0.0"
