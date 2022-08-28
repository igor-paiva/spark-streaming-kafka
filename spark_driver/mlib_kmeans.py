from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    explode,
    split,
    count,
    length,
    col,
    regexp_replace,
)
from pyspark.sql.types import StringType, ArrayType, StructType, StructField, FloatType

from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator

from nltk.metrics import distance


CLUSTERS_NUM = 5  # the k of KMeans
MAX_NUM_ROWS = 2147483647

spark = (
    SparkSession.builder.appName("StreamingWordCountKafka")
    .config("spark.sql.debug.maxToStringFields", "100")
    .getOrCreate()
)

lines = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-server:9092")
    .option("failOnDataLoss", "false")
    .option("subscribe", "sentences")
    .option("includeHeaders", "true")
    .option("startingOffsets", "earliest")  # latest
    .option("spark.streaming.kafka.maxRatePerPartition", "50")
    .load()
)

words = (
    lines.select("timestamp", explode(split(lines.value, " ")).alias("word"))
    .withColumn("word", regexp_replace(col("word"), r"[^a-zA-Z'-]", ""))
    .filter(length(col("word")) > 1)
)


def func(batch_df, batch_id):
    print(f"\nBatch ID: {batch_id}\n")

    words_list = list(map(lambda row: row.word, batch_df.collect()))

    dataset = [
        ([float(distance.edit_distance(w, _w)) for _w in words_list], w)
        for w in words_list
    ]

    schema = StructType(
        [
            StructField("features", ArrayType(FloatType(), containsNull=False), True),
            StructField("word", StringType(), True),
        ]
    )

    df = spark.createDataFrame(dataset, schema)

    kmeans = KMeans(k=CLUSTERS_NUM, seed=1)

    model = kmeans.fit(df)

    predictions = model.transform(df)

    predictions.select(count(predictions.word).alias("Total of words")).show()

    for k in range(CLUSTERS_NUM):
        print(f"\nCluster {k}:")

        cluster_data = predictions.filter(predictions.prediction == k)

        cluster_data.select(
            count(cluster_data.word).alias(f"Number of words in cluster {k}"),
        ).show()

        cluster_data.select(cluster_data.word.alias(f"Cluster {k} words")).show(
            MAX_NUM_ROWS
        )

    print("Model evaluation:\n")

    # Evaluate clustering by computing Silhouette score
    evaluator = ClusteringEvaluator()
    silhouette = evaluator.evaluate(predictions)
    print(f"\tSilhouette with squared euclidean distance: {silhouette} ([-1, 1])")

    # Evaluate clustering by computing Within Set Sum of Squared Errors
    wssse = model.summary.trainingCost
    print(f"\tWithin Set Sum of Squared Errors: {wssse}\n")


words.writeStream.foreachBatch(func).start().awaitTermination()
