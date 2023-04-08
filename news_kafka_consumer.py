import json
from kafka import KafkaConsumer
from kafka_util import KafkaUtil
import textblob as tb
import logging

def create_kafka_consumer(bootstrap_servers, topic):
    """Create a Kafka Consumer client.

    Args:
        bootstrap_servers (list): List of host/port pairs to use for establishing the initial connection to the Kafka cluster
        topic (str): Topic name

    Returns:
        KafkaConsumer: A Kafka Consumer client
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

def process_news_article(article):
    """Process news article.

    Args:
        article (dict): News article
    """
    if not article["title"]:
        return None
    blob = tb.TextBlob(article["title"])
    print(f"Title: {article['title']}, Polarity: {blob.sentiment.polarity}, Subjectivity: {blob.sentiment.subjectivity}")
    return {"title": article["title"], "source" : article["source"]["name"], "polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}


def consume_news(consumer, producer) -> dict:
    """Consume news articles from Kafka.

    Args:
        consumer (KafkaConsumer): A Kafka Consumer client
    """
    try:
        for message in consumer:
            sentiment_dict = process_news_article(message.value)
            if not sentiment_dict:
                continue
            producer.send("news_sentiment", sentiment_dict)
    except Exception as e:
        logging.error(f"Error while consuming messages: {e}")
    finally:
        consumer.close()

def main():
    bootstrap_servers = ["localhost:9092"]
    topic = "news"
    consumer = create_kafka_consumer(bootstrap_servers, topic)
    producer = KafkaUtil.create_kafka_producer(bootstrap_servers)
    consume_news(consumer, producer)

if __name__ == "__main__":
    main()

