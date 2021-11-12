FROM python:3.9-slim-buster
LABEL maintainer "Ulrich Genske <uli.genske@gmail.com>"
WORKDIR /home/HON
COPY requirements_docker.txt /home/HON
COPY . /home/HON
RUN apt-get update
RUN apt-get install -y libmariadb-dev
RUN apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements_docker.txt
RUN apt-get purge -y libmariadb-dev
RUN apt-get purge -y gcc
