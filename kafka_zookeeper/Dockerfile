FROM ubuntu:20.04

WORKDIR /kafka_zookeeper

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk procps

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

ENTRYPOINT [ "bash", "kafka_2.13-3.2.1/bin/zookeeper-server-start.sh", "kafka_2.13-3.2.1/config/zookeeper.properties" ]
