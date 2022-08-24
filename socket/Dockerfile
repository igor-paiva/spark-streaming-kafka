FROM ubuntu:20.04
FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

COPY . ./

RUN apt update

RUN apt install -y openjdk-11-jdk

RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc

RUN pip3 install -r requirements.txt

# RUN bash kafka_2.13-3.2.1/bin/kafka-topics.sh --create --topic sentences --bootstrap-server kafka-server:9092

# ENTRYPOINT [ "python3", "-u", "./main.py" ]

CMD tail -f /dev/null
