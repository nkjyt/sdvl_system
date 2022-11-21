FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

WORKDIR /work

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y -qq
RUN apt-get install python3 -y -qq
RUN apt-get install python3-pip -y -qq
RUN apt-get install apache2 -y -qq
RUN apt-get install vim -y -qq
RUN apt-get install libapache2-mod-wsgi-py3 -y -qq

COPY ./requirements.txt /work

RUN pip3 install -r requirements.txt

EXPOSE 80
