from kafka import KafkaProducer, KafkaConsumer
import os
import json

class KafkaUtil:
    @staticmethod
    def create_kafka_producer():
        return KafkaProducer(
            bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"],
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        )
    def create_kafka_consumer(topic):
        return KafkaConsumer(
            topic,
            bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"],
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )