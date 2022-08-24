# Parte 2 - Spark Streaming contabilizando palavras via Apache Kafka

## Sobre

Para executar será necessário ter instalado o `docker` e `docker-compose`.

## Como executar

### Iniciar os containers

```
docker-compose up
```

### Versão local

#### Iniciar o master

Em um novo terminal entre no container do master:

```
docker exec -it spark_kafka_master_1 bash
```

E inicie-o:

```
bash spark-3.1.3-bin-hadoop3.2/sbin/start-master.sh
```

#### Iniciar os workers

Em um novo terminal entre no container do worker 1:

```
docker exec -it spark_kafka_spark-worker-1_1 bash

# dentro do container
bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh spark://master:7077
```

Em um novo terminal entre no container do worker 2:

```
docker exec -it spark_kafka_spark-worker-2_1 bash

# dentro do container
bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh spark://master:7077
```

#### Iniciar o zookeeper

```
cd kafka_2.13-3.2.1

bash bin/zookeeper-server-start.sh config/zookeer.properties
```

#### Iniciar o servidor kafka

```
cd kafka_2.13-3.2.1

bash bin/kafka-server-start.sh config/server.properties
```

#### Criar o tópico

```
cd kafka_2.13-3.2.1

bin/kafka-topics.sh --create --topic sentences --bootstrap-server kafka-server:9092
```

# ------
# Faltou finalizar
# ------

<!-- #### Executar criação

```
``` -->

#### Submeter o problema

Em um novo terminal entre no container do submit:

```
docker exec -it spark_kafka_submit_1 bash
```

Para submeter o problema:

```
# pode ser qualquer arquivo

./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 local.py > results.txt
```
