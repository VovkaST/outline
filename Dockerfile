FROM python:3.10.17-bullseye
COPY ./ /app
WORKDIR /app

RUN apt-get update -y && \
    pip install -r requirements/base.txt
