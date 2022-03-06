# syntax=docker/dockerfile:1
FROM python:3.8.2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
CMD pytest