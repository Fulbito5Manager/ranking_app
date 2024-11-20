# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from unittest.mock import MagicMock, patch
# import unittest
# import pytest
# from services.kafka_consumer import consume_message
# from models.match_model import Match
# from flask import current_app
# from app import create_app  # Import your app creation method
# from utils.db import db  # Import the database

# class TestKafkaConsumer(unittest.TestCase):

#     def setUp(self):
#         """Set up the application context for each test"""
#         self.app = create_app('testing')  # Assuming you have a function to create your app
#         self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
#         self.app.config['TESTING'] = True
#         self.app_context = self.app.app_context()
#         self.app_context.push()
        
#         db.create_all()  # Create database tables for testing

#     def tearDown(self):
#         """Tear down the database and application context"""
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     @patch('services.kafka_consumer.get_message_from_kafka')  # Mock the wrapper function
#     def test_consume_message(self, mock_get_message):
#         # Simulate a Kafka message
#         mock_message = MagicMock()
#         mock_message.value.return_value = b'{"partido_id": 1, "date": "2024-09-06", "equipoganadorID": 2, "estado": "finished"}'
#         mock_message.topic.return_value = 'partidos-updates'
#         mock_message.error.return_value = None

#         # Set the mock to return the fake message
#         mock_get_message.return_value = mock_message

#         # Call the consume_message function with the mocked message
#         consume_message(mock_message)

#     """
    
#     Checks for components in Kafka and db at the same time.

#     INTEGRATION TEST. Integrating static code with a service. 

#     PRODUCER IDEA

#     """

#     @patch('services.kafka_consumer.get_message_from_kafka')
#     def test_kafka_event_and_db(self, mock_get_message):
#         # Step 1: Mock Kafka consumer to send a test event
#         with current_app.app_context():

#             mock_message = MagicMock()
#             mock_message.topic.return_value = 'partidos-updates'
#             mock_message.value.return_value = b'{"partido_id": 1, "date": "2024-09-06", "equipoganadorID": 2, "estado": "finished", "players_list": [1, 2, 3]}'
#             mock_message.error.return_value = None
            
#             # mock_kafka_consumer.return_value.poll.return_value = [mock_event]
#             mock_get_message.return_value = mock_message
#             # Step 2: Call the consumer function
#             consume_message(mock_message)

#             # Step 3: Verify the event was processed and stored in the database
#             match = Match.query.filter_by(id=1).first()

#             assert match is not None
#             assert match.players_list == [1, 2, 3]
#             # assert match.status == 'finished'

# if __name__ == '__main__':
#     unittest.main()
