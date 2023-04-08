import unittest
from unittest.mock import MagicMock
from news_kafka_producer import fetch_src_news, get_sources, send_news_to_kafka
from kafka import KafkaProducer

class TestNewsKafkaProducer(unittest.TestCase):
    def test_fetch_src_news(self):
        # Mock the NewsApiClient.get_everything method
        newsapi_mock = MagicMock()
        newsapi_mock.get_everything.return_value = {"status": "ok", "articles": [{"title": "Sample article"}]}
        
        source = "test_source"
        news_data = fetch_src_news(source, newsapi_mock)

        # Check if the function returns the expected news data
        self.assertEqual(len(news_data["articles"]), 1)
        self.assertEqual(news_data["articles"][0]["title"], "Sample article")

    def test_get_sources(self):
        # Mock the NewsApiClient.get_sources method
        newsapi_mock = MagicMock()
        newsapi_mock.get_sources.return_value = {"status": "ok", "sources": ["source1", "source2"]}

        sources = get_sources(newsapi_mock)

        # Check if the function returns the expected sources
        self.assertEqual(len(sources), 2)

    def test_send_news_to_kafka(self):
        # Mock the KafkaProducer.send method
        producer_mock = MagicMock(spec=KafkaProducer)

        news_data = {"articles": [{"title": "Sample article 1"}, {"title": "Sample article 2"}]}
        count = send_news_to_kafka(producer_mock, news_data)

        # Check if the function sends the expected number of messages
        self.assertEqual(count, 2)
        producer_mock.send.assert_called()


if __name__ == "__main__":
    unittest.main()