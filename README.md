# Parte 2 - Spark Streaming contabilizando palavras via Apache Kafka

Igor Batista Paiva - 18/0018728

## Sobre

Para executar será necessário ter instalado o `docker` e `docker-compose`.

## Configuração

Para instalar todas as dependências e criar todos os elementos necessários utilize o comando abaixo:

```
bash setup.sh
```

## Como executar

Após ter rodado o *setup* com sucesso para iniciar novamente só é necessário subir os containers e seguir os demais passos:

```
docker-compose up -d
```

Os containers sobem em modo *detach*, portanto caso queira ver os logs dos containers utilize:

```
docker-compose logs -f
```

### Iniciar o master

Será necessário iniciar o spark master:

```
docker exec -it spark_kafka_spark-master_1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-master.sh
```

### Iniciar os workers

Para iniciar os *workers*:

```
docker exec -it spark_kafka_spark-worker-1_1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://spark-master:7077 && docker exec -it spark_kafka_spark-worker-2_1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://spark-master:7077
```

### Iniciar o publisher

O publisher envia eventos para o servidor Kafka a cada meio segundo (0,5 segundo) com um paragrafo de texto.

Em um novo terminal (a chamada é blocante):

```
docker exec -it spark_kafka_kafka-publisher_1 bash

# dentro do container
python3 -u main.py
```

Para encerrar: `CTRL + C`.

### Submeter o problema

Em um novo terminal entre no container do spark driver:

```
docker exec -it spark_kafka_spark-driver_1 bash
```

Para submeter o problema utilize um dos comandos abaixo, o arquivo txt no final é para onde os resultados serão salvos.

#### Local

Para o modo local não é necessário iniciar o spark master e workers.

```
./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 local.py > results.txt
```

#### Cluster

```
./spark-3.1.3-bin-hadoop3.2/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 cluster.py > results.txt
```

## Resultados

Os resultados serão listados como tabelas com nomes de colunas descritivos no arquivo texto fornecido como saída para o comando `spark-submit`.

### Local e Cluster

Para ver o total de palavras processadas e quantidade de palavras no total é necessário ir ao final do arquivo e procurar por uma tabela com uma coluna "Total of words" e outra com as colunas "Word" e "Count".

Exemplo:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+--------------+
|Total of words|
+--------------+
|1672          |
+--------------+

-------------------------------------------
Batch: 0
-------------------------------------------
+--------------------+-----+
|Word                |Count|
+--------------------+-----+
|indicator           |1    |
|cheyenne            |1    |
|connected           |1    |
|recognize           |1    |
|By                  |3    |
|art                 |1    |
|carbonate           |1    |
|poetry              |1    |
|those               |2    |
|some                |2    |
+--------------------+-----+

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+-------------+
|Window                                    |Starts with R|
+------------------------------------------+-------------+
|{2022-08-27 01:42:03, 2022-08-27 01:42:06}|21           |
|{2022-08-27 01:40:18, 2022-08-27 01:40:21}|3            |
|{2022-08-27 01:41:57, 2022-08-27 01:42:00}|15           |
|{2022-08-27 01:41:54, 2022-08-27 01:41:57}|8            |
|{2022-08-27 01:42:00, 2022-08-27 01:42:03}|15           |
+------------------------------------------+-------------+

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+-------------+
|Window                                    |Starts with S|
+------------------------------------------+-------------+
|{2022-08-27 01:42:03, 2022-08-27 01:42:06}|38           |
|{2022-08-27 01:40:18, 2022-08-27 01:40:21}|2            |
|{2022-08-27 01:41:57, 2022-08-27 01:42:00}|27           |
|{2022-08-27 01:41:54, 2022-08-27 01:41:57}|14           |
|{2022-08-27 01:42:00, 2022-08-27 01:42:03}|43           |
+------------------------------------------+-------------+

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+-------------+
|Window                                    |Starts with P|
+------------------------------------------+-------------+
|{2022-08-27 01:42:03, 2022-08-27 01:42:06}|21           |
|{2022-08-27 01:40:18, 2022-08-27 01:40:21}|5            |
|{2022-08-27 01:41:57, 2022-08-27 01:42:00}|21           |
|{2022-08-27 01:41:54, 2022-08-27 01:41:57}|16           |
|{2022-08-27 01:42:00, 2022-08-27 01:42:03}|33           |
+------------------------------------------+-------------+

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+------------------------+
|Window                                    |Words with 11 characters|
+------------------------------------------+------------------------+
|{2022-08-27 01:42:03, 2022-08-27 01:42:06}|9                       |
|{2022-08-27 01:41:57, 2022-08-27 01:42:00}|9                       |
|{2022-08-27 01:41:54, 2022-08-27 01:41:57}|8                       |
|{2022-08-27 01:42:00, 2022-08-27 01:42:03}|22                      |
+------------------------------------------+------------------------+

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+-----------------------+
|Window                                    |Words with 6 characters|
+------------------------------------------+-----------------------+
|{2022-08-27 01:42:03, 2022-08-27 01:42:06}|48                     |
|{2022-08-27 01:40:18, 2022-08-27 01:40:21}|6                      |
|{2022-08-27 01:41:57, 2022-08-27 01:42:00}|30                     |
|{2022-08-27 01:41:54, 2022-08-27 01:41:57}|26                     |
|{2022-08-27 01:42:00, 2022-08-27 01:42:03}|49                     |
+------------------------------------------+-----------------------+

-------------------------------------------
Batch: 0
-------------------------------------------
+------------------------------------------+-----------------------+
|Window                                    |Words with 8 characters|
+------------------------------------------+-----------------------+
|{2022-08-27 01:42:03, 2022-08-27 01:42:06}|44                     |
|{2022-08-27 01:40:18, 2022-08-27 01:40:21}|5                      |
|{2022-08-27 01:41:57, 2022-08-27 01:42:00}|33                     |
|{2022-08-27 01:41:54, 2022-08-27 01:41:57}|30                     |
|{2022-08-27 01:42:00, 2022-08-27 01:42:03}|54                     |
+------------------------------------------+-----------------------+
```

### K-means (MLlib)

```
Batch ID: 0

+--------------+
|Total of words|
+--------------+
|          2180|
+--------------+


Cluster 0:
+----------------------------+
|Number of words in cluster 0|
+----------------------------+
|                         552|
+----------------------------+

+---------------+
|Cluster 0 words|
+---------------+
|        Equated|
|       employer|
|       revealed|
|        similar|
|        process|
|       catholic|
|       diffused|
|      attendees|
|       promoted|
|        concept|
|        alaskan|
|        muslims|
|      embedding|
...
+---------------+


Cluster 1:
+----------------------------+
|Number of words in cluster 1|
+----------------------------+
|                          29|
+----------------------------+

+--------------------+
|     Cluster 1 words|
+--------------------+
|     estates-general|
|      free-of-charge|
|       independently|
|     object-oriented|
|   census-designated|
|     fastest-growing|
|      Steel-skeleton|
|   Controlled-access|
|  telecommunications|
...
+--------------------+


Cluster 2:
+----------------------------+
|Number of words in cluster 2|
+----------------------------+
|                         902|
+----------------------------+

+---------------+
|Cluster 2 words|
+---------------+
|            led|
|             by|
|            the|
|             in|
|            two|
|           mohn|
|             By|
|            lds|
|            And|
|           east|
|            the|
|            and|
|            the|
...
+---------------+


Cluster 3:
+----------------------------+
|Number of words in cluster 3|
+----------------------------+
|                         211|
+----------------------------+

+---------------+
|Cluster 3 words|
+---------------+
|   afrocentrism|
|     protestant|
|   successfully|
|     Procedural|
|    Extravagant|
|   problematize|
...
+---------------+


Cluster 4:
+----------------------------+
|Number of words in cluster 4|
+----------------------------+
|                         486|
+----------------------------+

+---------------+
|Cluster 4 words|
+---------------+
|         virtue|
|          mbeki|
|         Murder|
|          rates|
...
+---------------+

Model evaluation:

	Silhouette with squared euclidean distance: 0.48074769822591146 ([-1, 1])
	Within Set Sum of Squared Errors: 4143810.344662394
```
