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
    SparkSession.builder.appName("StreamingWordCountKafka")
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
    total_words,
    words_count,
    starts_with_s,
    starts_with_r,
    starts_with_p,
    size_6,
    size_8,
    size_11,
]

i = 1

for df in data_frames:
    query = df.writeStream.start(
        outputMode="update",
        format="console",
        truncate=False,
        numRows=2147483647,  # to print as max rows as possible
    )

    if i == len(data_frames):
        query.awaitTermination()

    i += 1
