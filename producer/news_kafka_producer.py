import logging
import sys
from newsapi import NewsApiClient
from kafka import KafkaProducer
import json

def fetch_src_news(source: str, apinews: NewsApiClient):
    news_data = apinews.get_everything(
        q=" OR ".join(source),
        language="en",
        sort_by="publishedAt",
        page_size=100,
    )
    if news_data["status"] != "ok":
        return None
    return news_data

def get_sources(newsapi: NewsApiClient):
    sources = newsapi.get_sources()
    if sources["status"] != "ok":
        return None
    return sources["sources"]

def create_kafka_producer(bootstrap_servers: list):
    return  KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

def send_news_to_kafka(producer: KafkaProducer, news_data: dict):
    count = 0
    for article in news_data["articles"]:
        producer.send("news", article)
        count += 1
    return count


def main():
    newsapi = NewsApiClient(api_key='abf17ef31c434fbcbcd20521f497e7aa')

    sources: list = get_sources(newsapi)
    if not sources:
        logging.error("Error fetching sources")
        sys.exit(1)
    bootstrap_servers = ["localhost:9092"]
    producer = create_kafka_producer(bootstrap_servers)
    for source in sources:
        news_data = fetch_src_news(source, newsapi)
        if not news_data:
            logging.error(f"Error fetching news for {source}")
        logging.info(f"Successfully fetched {len(news_data['articles'])} news articles")
        count = send_news_to_kafka(producer, news_data)
        logging.info(f"Successfully sent {count} news articles to kafka")
    
    producer.flush()
    producer.close()

    logging.info(f"Finsihed fetching news articles from {len(sources)} sources ")

if __name__ == "__main__":
    main()
