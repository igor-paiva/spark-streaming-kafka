import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
from essential_generators import DocumentGenerator


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=["kafka-server:9092"])
    gen = DocumentGenerator()

    while True:
        try:
            message = gen.paragraph()

            producer.send("sentences", message.encode("utf-8"))

            print(f"\n{message}\n")

            time.sleep(0.5)
        except KafkaError as e:
            print(e)
            break
