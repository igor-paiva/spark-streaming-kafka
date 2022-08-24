FROM ubuntu:20.04
FROM python:3.7-slim

WORKDIR /submit

USER root

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk

RUN echo 'export SPARK_HOME=/submit/spark-3.1.3-bin-hadoop3.2' >> ~/.bashrc

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

# RUN pip3 install pyspark==3.1.3
RUN pip3 install -r requirements.txt --user

CMD tail -f /dev/null
