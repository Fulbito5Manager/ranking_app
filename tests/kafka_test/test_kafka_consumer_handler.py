import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from unittest.mock import MagicMock, patch
import unittest
from flask import current_app
from app import create_app 
from utils.db import db
import json
from kafka_handler import KafkaConsumerHandler

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

    @patch('kafka_handler.KafkaConsumerHandler.get_message_from_kafka')  # Mock the wrapper function
    def test_consume_message(self, mock_get_message):

        event_data = {
            "eventType": "MATCH_FINISHED",
            "data": {
                "match_id": 1,
                "date": "2024-09-06",
                "equipoganadorID": 2,
                "estado": "finished"
            }
        }

        mock_message = MagicMock()
        mock_message.value.return_value = json.dumps(event_data).encode('utf-8')
        mock_message.topic.return_value = 'match_service_topic'
        mock_message.error.return_value = None

        mock_get_message.return_value = mock_message

        consumer_handler = KafkaConsumerHandler(topics=['match_service_topic'], app_context=self.app_context)

        consumer_handler._process_message(mock_message)