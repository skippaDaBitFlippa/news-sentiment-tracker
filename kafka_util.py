from kafka import KafkaProducer, KafkaConsumer
import json

class KafkaUtil:
    @staticmethod
    def create_kafka_producer(bootstrap_servers):
        return KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        )
    def create_kafka_consumer(bootstrap_servers, topic):
        return KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )