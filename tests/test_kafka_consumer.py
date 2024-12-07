import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, patch
import unittest
from kafka_handler.kafka_consumer import consume_message
from models.match_model import Match
from flask import current_app
from app import create_app  # Import your app creation method
from utils.db import db  # Import the database
import json

class TestKafkaConsumer(unittest.TestCase):

    def setUp(self):
        """Set up the application context for each test"""
        self.app = create_app('testing')  # Assuming you have a function to create your app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()  # Create database tables for testing

    def tearDown(self):
        """Tear down the database and application context"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('services.kafka_consumer.get_message_from_kafka')  # Mock the wrapper function
    def test_consume_message(self, mock_get_message):
        # Construct valid JSON using Python objects
        event_data = {
            "Event_type": "MATCH_FINISHED",
            "data": {  
                "Match_id": 1,
                "date": "2024-09-06",
                "equipoganadorID": 2,
                "estado": "finished"
            }
        }

        mock_message = MagicMock()
        mock_message.value.return_value = json.dumps(event_data).encode('utf-8')
        mock_message.topic.return_value = 'partidos-updates'
        mock_message.error.return_value = None

        mock_get_message.return_value = mock_message

        consume_message(mock_message)
        

    @patch('services.kafka_consumer.get_message_from_kafka')  # Mock the wrapper function
    def test_consume_message_empty_message(self, mock_get_message):
        # Construct valid JSON using Python objects
        event_data = {
            "Event_type": "MATCH_FINISHED",
            "data": {  
            }
        }
        # Mock Kafka message with valid JSON
        mock_message = MagicMock()
        mock_message.value.return_value = json.dumps(event_data).encode('utf-8')
        mock_message.topic.return_value = 'partidos-updates'
        mock_message.error.return_value = None

        # Set the mock to return the fake message
        mock_get_message.return_value = mock_message

        # Call the consume_message function with the mocked message
        consume_message(mock_message)
    
    @patch('services.kafka_consumer.get_message_from_kafka')  # Mock the wrapper function
    def test_consume_message_invalid_event_type(self, mock_get_message):
        # Construct valid JSON using Python objects
        event_data = {
            "Event_type": "MATCH_CANCELED",
            "data": {  
            }
        }
        # Mock Kafka message with valid JSON
        mock_message = MagicMock()
        mock_message.value.return_value = json.dumps(event_data).encode('utf-8')
        mock_message.topic.return_value = 'partidos-updates'
        mock_message.error.return_value = None

        # Set the mock to return the fake message
        mock_get_message.return_value = mock_message

        # Call the consume_message function with the mocked message
        consume_message(mock_message)

    @patch('services.kafka_consumer.get_message_from_kafka')  # Mock the wrapper function
    def test_consume_message_invalid_json_data(self, mock_get_message):
        # Construct valid JSON using Python objects
        event_data = None
        # Mock Kafka message with valid JSON
        mock_message = MagicMock()
        mock_message.value.return_value = None
        mock_message.topic.return_value = 'partidos-updates'
        mock_message.error.return_value = None

        # Set the mock to return the fake message
        mock_get_message.return_value = mock_message

        # Call the consume_message function with the mocked message
        consume_message(mock_message)


if __name__ == '__main__':
    unittest.main()
