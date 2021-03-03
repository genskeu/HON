FROM python:3.6-slim-buster
WORKDIR /HON_full

# conda env
COPY requirments.txt ./
RUN pip install --upgrade pip
RUN pip3 install -r ./requirments.txt

# app folders with APP, tests ....
COPY HON ./HON
COPY wsgi.py ./
COPY config.py ./config.py
ENV FLASK_APP=HON

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# initilize db
#RUN mkdir instance
RUN flask init-db


