echo "Creating docker network"

docker network create spark-cluster || true

echo "Downloading Spark 3.1.3"

wget https://dlcdn.apache.org/spark/spark-3.1.3/spark-3.1.3-bin-hadoop3.2.tgz

tar xzf spark-3.1.3-bin-hadoop3.2.tgz

rm spark-3.1.3-bin-hadoop3.2.tgz

echo "Downloading Kafka 3.2.1"

wget https://downloads.apache.org/kafka/3.2.1/kafka_2.13-3.2.1.tgz

tar xzf kafka_2.13-3.2.1.tgz

rm kafka_2.13-3.2.1.tgz

echo "Initializing containers"

docker-compose up -d

echo "Creating kafka 'sentences' topic"

# to create "sentences" topic
docker exec -it spark_kafka_socket_1 bash kafka_2.13-3.2.1/bin/kafka-topics.sh --create --topic sentences --bootstrap-server kafka-server:9092

echo "Stoping containers"

docker-compose stop
