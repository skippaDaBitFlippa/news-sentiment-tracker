import unittest
from unittest.mock import patch
from kafka import KafkaProducer
from kafka_util import KafkaUtil


class TestConsumer(unittest.TestCase):
    def test_create_kafka_producer(self):
            with patch("kafka.KafkaProducer.__init__", return_value=None):
                bootstrap_servers = ["localhost:9092"]
                producer = KafkaUtil.create_kafka_producer(bootstrap_servers)

                # Check if the KafkaProducer instance is created
                self.assertIsInstance(producer, KafkaProducer)