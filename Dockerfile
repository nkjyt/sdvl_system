FROM ubuntu:20.04

WORKDIR /app

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y -qq
RUN apt-get install python3 -y -qq
RUN apt-get install python3-pip -y -qq
RUN apt-get install vim -y -qq
RUN apt-get install wget -y -qq


COPY ./app/requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 80
