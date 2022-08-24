FROM ubuntu:20.04

WORKDIR /worker

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk procps

RUN echo 'export SPARK_HOME=/worker/spark-3.1.3-bin-hadoop3.2' >> ~/.bashrc

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

# ENTRYPOINT ["bash", "spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh", "-m 1G", "-c 1", "spark://master:7077"]

CMD tail -f /dev/null
