import unittest
from unittest.mock import MagicMock, patch
from news_kafka_consumer import process_news_article, consume_news
from kafka import KafkaConsumer, KafkaProducer
from kafka.consumer.fetcher import ConsumerRecord

class TestConsumer(unittest.TestCase):
    def test_process_news_article(self):
        article = {"title": "Sample article", "source": {"name": "Sample Source"}}
        result = process_news_article(article)
        self.assertEqual(result, {
            "title": "Sample article",
            "source": "Sample Source",
            "polarity": 0.0,
            "subjectivity": 0.0
        })
    
    def test_process_news_article_with_none_title(self):
        article = {"title": None}

        with patch("builtins.print") as print_mock:
            actual = process_news_article(article)

            # Assert that the print function is not called
            self.assertIsNone(actual)

    def test_consume_news(self):
        # Mock the KafkaConsumer instance and its iterator
        consumer_mock = MagicMock(spec=KafkaConsumer)
        record_mock = ConsumerRecord(
            topic="news",
            partition=0,
            offset=0,
            timestamp=0,
            timestamp_type=0,
            key=None,
            value={"title": "Sample article", "source": {"name": "Sample Source"}},
            headers=[],
            checksum=None,
            serialized_key_size=-1,
            serialized_value_size=-1,
            serialized_header_size=-1
        )
        iterator_mock = MagicMock()
        iterator_mock.__iter__.return_value = [record_mock]
        consumer_mock.__iter__.return_value = iterator_mock

        producer_mock = MagicMock(spec=KafkaProducer)

        with patch("news_kafka_consumer.process_news_article") as process_news_article_mock:
            process_news_article_mock.return_value = {
                "title": "Sample article",
                "source": "Sample Source",
                "polarity": 0.5,
                "subjectivity": 0.1
            }

            consume_news(consumer_mock, producer_mock)
            process_news_article_mock.assert_called_with({"title": "Sample article", "source": {"name": "Sample Source"}})
            producer_mock.send.assert_called_with("news_sentiment", {
                "title": "Sample article",
                "source": "Sample Source",
                "polarity": 0.5,
                "subjectivity": 0.1
            })
            

if __name__ == "__main__":
    unittest.main()