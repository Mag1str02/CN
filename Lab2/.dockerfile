FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y iputils-ping
RUN apt-get install -y python3-all 
RUN mkdir -p /usr/src/ping
COPY ./pmtu_disc.py  /usr/src/ping
WORKDIR /usr/src/ping