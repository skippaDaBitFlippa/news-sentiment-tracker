from kafka import KafkaProducer
import json

class KafkaUtil:
    @staticmethod
    def create_kafka_producer(bootstrap_servers):
        return KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        )