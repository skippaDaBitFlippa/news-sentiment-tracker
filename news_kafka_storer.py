from kafka_util import KafkaUtil
from kafka import KafkaConsumer
import psycopg2
from psycopg2 import sql
import logging
import os

INSERT_QUERY = sql.SQL("""
        INSERT INTO news_sentiment (title, timestamp, source, polarity, subjectivity)
        VALUES (%s, TO_TIMESTAMP(%s, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC', %s, %s, %s)
        ON CONFLICT DO NOTHING
    """)
def connect_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def store_messages(consumer: KafkaConsumer, connection: psycopg2.extensions.connection):
    cursor = connection.cursor()
    for message in consumer:
        print(message.value)
        info = message.value
        cursor.execute(INSERT_QUERY, (info["title"], info["publishedAt"], info["source"], info["polarity"], info["subjectivity"]))
        connection.commit()
        logging.info(f"Stored message: {message.value}")
    cursor.close()



def main():
    topic = "news_sentiment"
    consumer = KafkaUtil.create_kafka_consumer(topic)
    connection = connect_db()
    store_messages(consumer, connection)
    connection.close()

if __name__ == "__main__":
    main()

