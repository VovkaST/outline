FROM python:3.10.17-bookworm
COPY ./ /app
WORKDIR /app

RUN pip install -r requirements/base.txt
