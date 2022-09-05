FROM ubuntu:20.04

WORKDIR /spark-worker

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk procps

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

RUN echo 'export SPARK_HOME=/spark-worker/spark-3.1.3-bin-hadoop3.2' >> ~/.bashrc

CMD tail -f /dev/null
