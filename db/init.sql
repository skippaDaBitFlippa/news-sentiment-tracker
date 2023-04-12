CREATE TABLE news_sentiment (
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    polarity REAL NOT NULL,
    subjectivity REAL NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (source, timestamp)
);
