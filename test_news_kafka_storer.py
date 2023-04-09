import unittest
from unittest.mock import MagicMock, patch
from news_kafka_storer import connect_db, store_messages, INSERT_QUERY
from psycopg2 import OperationalError
from kafka import KafkaConsumer

class TestNewsKafkaStorer(unittest.TestCase):

    @patch("psycopg2.connect")
    def test_connect_db(self, mock_connect):
        # Test successful connection
        mock_connect.return_value = "mock_connection"
        connection = connect_db()
        self.assertEqual(connection, "mock_connection")

        # Test failed connection
        mock_connect.side_effect = OperationalError("Failed to connect")
        with self.assertRaises(OperationalError):
            connect_db()

    def test_store_messages(self):
        mock_consumer = MagicMock(spec=KafkaConsumer)
        mock_message = MagicMock()
        mock_message.value = {
            'title': 'Test Title',
            'publishedAt': '2023-04-07T23:47:32Z',
            'source': 'Test Source',
            'polarity': 0.1,
            'subjectivity': 0.5
        }
        mock_consumer.__iter__.return_value = [mock_message]

        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value

        store_messages(mock_consumer, mock_connection)

        mock_cursor.execute.assert_called_once_with(INSERT_QUERY, (
            mock_message.value["title"],
            mock_message.value["publishedAt"],
            mock_message.value["source"],
            mock_message.value["polarity"],
            mock_message.value["subjectivity"]
        ))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()