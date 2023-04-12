from kafka_util import KafkaUtil
import textblob as tb
import logging
from kafka_util import KafkaUtil

def process_news_article(article):
    """Process news article.

    Args:
        article (dict): News article
    """
    if not article["title"]:
        return None
    blob = tb.TextBlob(article["title"])
    return {"title": article["title"], "publishedAt": article["publishedAt"], "source" : article["source"]["name"], "polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}


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
    topic = "news"
    consumer = KafkaUtil.create_kafka_consumer(topic)
    producer = KafkaUtil.create_kafka_producer()
    consume_news(consumer, producer)

if __name__ == "__main__":
    main()

