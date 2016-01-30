FROM ubuntu:latest

RUN apt-get update && \
	apt-get install -y python3.4 python3.4-dev python3-pip && \
	rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip3 install -r requirements.txt

COPY . /usr/src/app
