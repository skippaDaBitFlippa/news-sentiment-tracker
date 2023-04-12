import os
import unittest
from unittest.mock import patch
from kafka import KafkaProducer, KafkaConsumer
from kafka_util import KafkaUtil

class TestConsumer(unittest.TestCase):
    def test_create_kafka_producer(self):
        with patch("kafka.KafkaProducer.__init__", return_value=None), \
            patch.dict(os.environ, {"KAFKA_BOOTSTRAP_SERVERS": "localhost:9092"}):
            producer = KafkaUtil.create_kafka_producer()
            # Check if the KafkaProducer instance is created
            self.assertIsInstance(producer, KafkaProducer)

    def test_create_kafka_consumer(self):
        with patch("kafka.KafkaConsumer.__init__", return_value=None), \
            patch.dict(os.environ, {"KAFKA_BOOTSTRAP_SERVERS": "localhost:9092"}):
            topic = "news"
            consumer = KafkaUtil.create_kafka_consumer(topic)
            self.assertIsInstance(consumer, KafkaConsumer)