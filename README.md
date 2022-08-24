# Parte 2 - Spark Streaming contabilizando palavras via Apache Kafka

## Sobre

Para executar será necessário ter instalado o `docker` e `docker-compose`.

## Como executar

### Iniciar os containers

```
bash start.sh

# caso a rede do docker já exista a mensagem "Error response from daemon: network with name spark-cluster already exists" vai ser imprimida, porém não é um erro.
```

Os containers sobem em modo *detach*, portanto caso queira ver os logs dos containers utilize:

```
docker-compose logs -f
```

### Iniciar o master

Será necessário iniciar o spark master:

```
docker exec -it spark_kafka_master_1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-master.sh
```

### Iniciar os workers

Para iniciar os *workers*:

```
docker exec -it spark_kafka_spark-worker-1_1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://master:7077 && docker exec -it spark_kafka_spark-worker-2_1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://master:7077
```

<!-- ### Criar o tópico

```
cd kafka_2.13-3.2.1

bin/kafka-topics.sh --create --topic sentences --bootstrap-server kafka-server:9092
``` -->

### Iniciar o publisher

O publisher envia eventos para o servidor Kafka a cada meio segundo (0,5 segundo) com um paragrafo de texto.

Em um novo terminal (a chada é blocante):

```
docker exec -it spark_kafka_socket_1 bash

# dentro do container
python3 -u main.py
```

Para encerrar `CTRL + C`

### Submeter o problema

Em um novo terminal entre no container do submit:

```
docker exec -it spark_kafka_submit_1 bash
```

Para submeter o problema utilize um dos comandos abaixo, o arquivo txt no final é para onde os resultados serão salvos.

#### Local

Para o modo local não é necessário iniciar o spark master e workers.

```
./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 local.py > results.txt
```

#### Cluster

```
./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 cluster.py > results.txt
```
