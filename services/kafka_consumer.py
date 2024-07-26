from kafka import KafkaConsumer
import json
from app.controller import handle_event

consumer = KafkaConsumer('player_events', bootstrap_servers='localhost:9092')

for message in consumer:
    event_data = json.loads(message.value.decode('utf-8'))
    player_view, ranking_view = handle_event(event_data)
    print(player_view.get_json())
    print(ranking_view.get_json())