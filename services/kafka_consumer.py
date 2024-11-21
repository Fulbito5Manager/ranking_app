from confluent_kafka import Consumer, KafkaError
import json
from services.ranking_service import calculate_player_ranking
from settings import BOOTSTRAP_SERVER_RUNNING, KAFKA_GROUP_ID
import threading
from app import create_app

app = create_app()

EVENTTYPE_MATCH_FINISHED = "MATCH_FINISHED"

consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVER_RUNNING,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': 'earliest'
})

topics = ['partidos-updates']
consumer.subscribe(topics)

def get_message_from_kafka(consumer, timeout=1.0):
    """ A wrapper to poll a message from Kafka """
    return consumer.poll(timeout=timeout)

def handle_partidos_update(match_event_data):
    try:
        event_type = match_event_data.get('Event_type')
        
        if event_type == EVENTTYPE_MATCH_FINISHED:
            match_id = match_event_data['data'].get('Match_id')
            calculate_player_ranking(match_id)
        else:
            print(f"Error handling partido update: {e}")

    except Exception as e:
        print(f"Error handling partido update: {e}")

def consume_loop():
    try:
        while True:
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

# {
#     Event_type: MATCH_FINISHED, 
#     data:{
#         Match_id: 1
#     }
# }