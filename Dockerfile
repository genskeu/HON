FROM python:3.6-slim-buster
WORKDIR /HON_full

# conda env
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

# app folders with APP, tests ....
COPY app ./app
COPY wsgi.py ./
COPY config.py ./config.py
ENV FLASK_ENV=docker

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# initilize db
#RUN mkdir instance
RUN flask init-db


