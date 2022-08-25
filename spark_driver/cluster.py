from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, initcap, count, length

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

words = lines.select(explode(split(lines.value, " ")).alias("word"))

total_words = words.select(count(words.word).alias("Total of words"))

starts_with_s = words.select(initcap("word").alias("Start with S")).filter(
    words.word.startswith("S")
)

starts_with_r = words.select(initcap("word").alias("Start with R")).filter(
    words.word.startswith("R")
)

starts_with_p = words.select(initcap("word").alias("Start with P")).filter(
    words.word.startswith("P")
)

size_6 = (
    words.select(words.word, length(words.word).alias("length"))
    .filter("length == 6")
    .select(words.word.alias("Words as Words with 6 characters"))
)

size_8 = (
    words.select(words.word, length(words.word).alias("length"))
    .filter("length == 8")
    .select(words.word.alias("Words as Words with 8 characters"))
)

size_11 = (
    words.select(words.word, length(words.word).alias("length"))
    .filter("length == 11")
    .select(words.word.alias("Words as Words with 11 characters"))
)

data_frames = [
    total_words,
    starts_with_s,
    starts_with_r,
    starts_with_p,
    size_6,
    size_8,
    size_11,
]

i = 1

for df in data_frames:
    query = (
        df.writeStream.option("numRows", 500)
        .outputMode("update")
        .format("console")
        .start()
    )

    if i == len(data_frames):
        query.awaitTermination()

    i += 1
