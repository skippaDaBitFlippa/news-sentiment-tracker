# news-sentiment-tracker
This is a simple news app that uses Kafka to stream news articles and calculate sentiment scores. It consists of three main components:

News Kafka Producer: fetches news articles from a news API and sends them to a Kafka topic.
News Kafka Consumer: consumes news articles from a Kafka topic, calculates sentiment scores using TextBlob, and sends them to another Kafka topic.
News Kafka Storer: consumes sentiment scores from a Kafka topic, stores them in a PostgreSQL database, and calculates the average sentiment score for each news source over a specified time window.