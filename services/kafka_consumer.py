from confluent_kafka import Consumer, KafkaException
import requests, json
from services.match_service import create_match, get_winner_team_id_by_match_id
from services.player_service import bring_old_and_new_players, update_old_players, handle_new_players, calculate_player_ranking
from config import BOOTSTRAP_SERVER_RUNNING, KAFKA_GROUP_ID
import threading
from confluent_kafka import KafkaError, KafkaException
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

    try:
        match_status = match_event_data.get('estado')
        
        print("Handle partido update message received. match_event_data: ", match_event_data)

        if match_status == MATCH_STATUS_FINISHED:

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
                # Si es el final de la partición, lo manejamos y continuamos
                if message.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {message.topic()} [{message.partition()}] at offset {message.offset()}")
                    continue
                else:
                    # Si es otro tipo de error, lo mostramos y rompemos el loop
                    print(f"Error: {message.error()}")
                    break

            # Use the app context to handle the message
            with app.app_context():
                try:
                    consume_message(message)  # Your message processing logic
                except Exception as e:
                    print(f"Error handling message: {str(e)}")

    finally:
        consumer.close()

def consume_message(message):
    """ Function to handle a single message """
    try:
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


"""
Missing matches function. Not applicable for an optimistic approach
"""
# def check_for_missing_matches(player_id):
#     # Get matches from API
#     matches_list = get_matches()
#     # Filter matches Id from API by finished matches
#     matches_list_id_api = [match['id'] for match in matches_list if match['status'] == "finished"]

#     # Get matches from DB to later compare
#     matches_db = Match.filter_by_player(player_id)
#     #Filter by id
#     match_list_id_db = [match.id for match in matches_db]

#     #Convert them to set for comparisong
#     total_matches_api = set(matches_list_id_api)
#     total_matches_db = set(match_list_id_db)

#     # Just a simple check
#     if total_matches_api == total_matches_db:
#         print({"status": "Matches are in sync"})
#     else:
#         # Handle the mismatch case, perhaps by syncing the data
#         print({"status": "Mismatch found", "api_matches": list(total_matches_api), "db_matches": list(total_matches_db)})
    
#     missing_matches = list(total_matches_api - total_matches_db) # Careful with set 

#     found_player = Player.query.filter_by(id=player_id).first()
#     rankings = []
#     # If missing data we can added to players db points

#     if missing_matches:
        
#         for match_id in missing_matches:
#             response = requests.get(f'http://localhost:5000/rank/{player_id}/{match_id}')
#             if response.status_code == 200: # If sucess
#                 ranking_data = response.json()
#                 rankings.append(ranking_data)
    
#         if found_player:
#             for rankings.points in rankings:
#                 found_player.points += rankings['points']
#                 # Also we can bring rank check from ranking service to check if "rank" was upgraded.

#             db.session.commit()

#         return {"rank": found_player.points, "points": found_player.points}