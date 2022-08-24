docker network create spark-cluster || true

docker-compose up -d

# to create "sentences" topic
docker exec -it spark_kafka_socket_1 bash kafka_2.13-3.2.1/bin/kafka-topics.sh --create --topic sentences --bootstrap-server kafka-server:9092
