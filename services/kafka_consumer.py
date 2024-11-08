from confluent_kafka import Consumer, KafkaError
import requests, json
from services.match_service import create_match, get_winner_team_id_by_match_id
from services.player_service import calculate_player_ranking
from settings import BOOTSTRAP_SERVER_RUNNING, KAFKA_GROUP_ID
import threading
from app import create_app
from models.player_model import Player

app = create_app()

MATCH_STATUS_FINISHED = "finished"

# Consumer setup
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVER_RUNNING,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': 'earliest'
})

# Subscribe to the topics
topics = ['partidos-updates'] #'equipos-updates', "jugadores-service-update", jugadores-service-update
consumer.subscribe(topics)

def get_message_from_kafka(consumer, timeout=1.0):
    """ A wrapper to poll a message from Kafka """
    return consumer.poll(timeout=timeout)

def handle_partidos_update(match_event_data): # I will only get Partido ID

    # print("Handle partido update message received. match_event_data: ", match_event_data)
    print(match_event_data)
    try:
        match_status = match_event_data.get('estado')
        
        # print("Handle partido update message received. match_event_data: ", match_event_data['partidoID'])

        if match_status == MATCH_STATUS_FINISHED:
            print("Handle partido update message received. match_event_data: ", match_event_data)
            calculate_player_ranking(match_event_data['partidoID'])

    except Exception as e:
        print(f"Error handling partido update: {e}")

def consume_loop():
    try:
        while True:
            # print("Listening messages, in loop.")
            message = get_message_from_kafka(consumer)
            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {message.topic()} [{message.partition()}] at offset {message.offset()}")
                    continue
                else:
                    print(f"Error: {message.error()}")
                    break

            with app.app_context():
                try:
                    consume_message(message)
                except Exception as e:
                    print(f"Error handling message: {str(e)}")

    finally:
        consumer.close()

def consume_message(message):
    """ Function to handle a single message """
    try:
        raw_data = message.value()
        if raw_data is None:
            print("Received an empty message.")
            return
        
        # Deserialize the message value
        data = json.loads(message.value().decode('utf-8'))
        print('data:', data)

        # Handle the message based on the topic
        if message.topic() == 'partidos-updates':
            handle_partidos_update(data)
        # Add more conditions if needed for other topics

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def start_kafka_consumer():
    consumer_thread = threading.Thread(target=consume_loop)
    consumer_thread.daemon = True  # Para que se cierre cuando la app Flask se cierre
    consumer_thread.start()
