from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    explode,
    split,
    initcap,
    count,
    length,
    window,
    col,
    lit,
    current_timestamp,
)

spark = (
    SparkSession.builder.master("spark://spark-master:7077")
    .appName("StreamingWordCountKafkaDistributed")
    .config("spark.driver.host", "spark-driver")
    # .config("spark.driver.port", "5005")
    .config("spark.dynamicAllocation.enabled", "false")
    .config("spark.shuffle.service.enabled", "false")
    .config("spark.streaming.driver.writeAheadLog.closeFileAfterWrite", "true")
    .config("spark.streaming.receiver.writeAheadLog.closeFileAfterWrite", "true")
    .config("spark.executor.memory", "512m")
    .config("spark.executor.instances", "2")
    .config("spark.pyspark.python", "python3")
    .config("spark.pyspark.driver.python", "python3")
    .config("spark.sql.debug.maxToStringFields", "100")
    .getOrCreate()
)

# spark_context = spark.sparkContext
# spark_context.checkpoint("hdfs://hadoop:9000/checkpoint")

lines = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-server:9092")
    # .option("kafka.security.protocol", "SSL")
    .option("failOnDataLoss", "false")
    .option("subscribe", "sentences")
    .option("includeHeaders", "true")
    .option("startingOffsets", "earliest")  # latest
    .option("spark.streaming.kafka.maxRatePerPartition", "50")
    .load()
)

words = lines.select(explode(split(lines.value, " ")).alias("word")).withColumn(
    "timestamp", lit(current_timestamp())
)

# current_timestamp().alias("Timestamp")
total_words = words.select(count(words.word).alias("Total of words"))

words_count = (
    words.groupBy("word")
    .count()
    .select(col("word").alias("Word"), col("count").alias("Count"))
    # current_timestamp().alias("Timestamp")
)

starts_with_s = (
    words.filter(initcap(words.word).startswith("S"))
    .groupBy(window("timestamp", "3 seconds", "3 seconds"))
    .count()
    .select(col("window").alias("Window"), col("count").alias("Starts with S"))
)

starts_with_r = (
    words.filter(initcap(words.word).startswith("R"))
    .groupBy(window("timestamp", "3 seconds", "3 seconds"))
    .count()
    .select(col("window").alias("Window"), col("count").alias("Starts with R"))
)

starts_with_p = (
    words.filter(initcap(words.word).startswith("P"))
    .groupBy(window("timestamp", "3 seconds", "3 seconds"))
    .count()
    .select(col("window").alias("Window"), col("count").alias("Starts with P"))
)

size_6 = (
    words.filter(length(words.word) == 6)
    .groupBy(window("timestamp", "3 seconds", "3 seconds"))
    .count()
    .select(
        col("window").alias("Window"), col("count").alias("Words with 6 characters")
    )
)

size_8 = (
    words.filter(length(words.word) == 8)
    .groupBy(window("timestamp", "3 seconds", "3 seconds"))
    .count()
    .select(
        col("window").alias("Window"), col("count").alias("Words with 8 characters")
    )
)

size_11 = (
    words.filter(length(words.word) == 11)
    .groupBy(window("timestamp", "3 seconds", "3 seconds"))
    .count()
    .select(
        col("window").alias("Window"), col("count").alias("Words with 11 characters")
    )
)

data_frames = [
    (total_words, "complete"),
    (words_count, "complete"),
    (starts_with_s, "update"),
    (starts_with_r, "update"),
    (starts_with_p, "update"),
    (size_6, "update"),
    (size_8, "update"),
    (size_11, "update"),
]

i = 1

for data in data_frames:
    df, mode = data

    query = df.writeStream.start(
        outputMode=mode,
        format="console",
        truncate=False,
        numRows=2147483647,  # to print as max rows as possible
    )

    if i == len(data_frames):
        query.awaitTermination()

    i += 1
