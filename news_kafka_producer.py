import sys
import logging
import schedule
import time
from newsapi import newsapi_client
from kafka_util import KafkaUtil
from kafka import KafkaProducer

def fetch_src_news(source: str, news_client):
    news_data = news_client.get_everything(
        q=" OR ".join(source),
        language="en",
        sort_by="publishedAt",
        page_size=100,
    )
    if news_data["status"] != "ok":
        return None
    return news_data

def get_sources(news_client):
    sources = news_client.get_sources()
    if sources["status"] != "ok":
        return None
    return sources["sources"]

def send_news_to_kafka(producer: KafkaProducer, news_data: dict):
    count = 0
    for article in news_data["articles"]:
        producer.send("news", article)
        count += 1
    return count


def news_api_job():
    news_client = newsapi_client.NewsApiClient(api_key='<NEWS-API_KEY>')

    sources: list = get_sources(news_client)
    if not sources:
        logging.error("Error fetching sources")
        sys.exit(1)
    producer = KafkaUtil.create_kafka_producer()
    for source in sources:
        news_data = fetch_src_news(source, news_client)
        if not news_data:
            logging.error(f"Error fetching news for {source}")
        logging.info(f"Successfully fetched {len(news_data['articles'])} news articles")
        count = send_news_to_kafka(producer, news_data)
        logging.info(f"Successfully sent {count} news articles to kafka")
    
    producer.flush()
    producer.close()

    logging.info(f"Finsihed fetching news articles from {len(sources)} sources ")

def main():
    schedule.every(30).seconds.do(news_api_job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
