import unittest
from unittest.mock import MagicMock, patch
from news_kafka_consumer import create_kafka_consumer, process_news_article, consume_news
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

class TestConsumer(unittest.TestCase):
    def test_create_kafka_consumer(self):
        with patch("kafka.KafkaConsumer.__init__", return_value=None):
            bootstrap_servers = ["localhost:9092"]
            topic = "news"
            consumer = create_kafka_consumer(bootstrap_servers, topic)
            self.assertIsInstance(consumer, KafkaConsumer)

    def test_process_news_article(self):
        article = {"title": "Sample article"}

        with patch("builtins.print") as print_mock, patch("textblob.blob.TextBlob.sentiment", new_callable=MagicMock) as sentiment_mock:
            sentiment_mock.polarity = 0.5
            sentiment_mock.subjectivity = 0.1
            process_news_article(article)
            print_mock.assert_called_with("Title: Sample article, Polarity: 0.5, Subjectivity: 0.1")
    
    def test_process_news_article_with_none_title(self):
        article = {"title": None}

        with patch("builtins.print") as print_mock:
            process_news_article(article)

            # Assert that the print function is not called
            print_mock.assert_not_called()

    def test_consume_news(self):
        # Mock the KafkaConsumer instance and its iterator
        consumer_mock = MagicMock(spec=KafkaConsumer)
        iterator_mock = MagicMock()
        
        # Create a mocked ConsumerRecord object
        record = ConsumerRecord(
            topic="news",
            partition=0,
            offset=0,
            timestamp=0,
            timestamp_type=0,
            key=None,
            value={"title": "Sample article"},
            headers=[],
            checksum=None,
            serialized_key_size=-1,
            serialized_value_size=-1,
            serialized_header_size=-1
        )

        iterator_mock.__iter__.return_value = [record]
        consumer_mock.__iter__.return_value = iterator_mock

        with patch("news_kafka_consumer.process_news_article") as process_news_article_mock:
            consume_news(consumer_mock)
            print("consume_news function completed")
            process_news_article_mock.assert_called_with({"title": "Sample article"})

if __name__ == "__main__":
    unittest.main()