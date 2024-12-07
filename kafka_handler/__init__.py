from confluent_kafka import Consumer, KafkaError
import threading, json
from settings import BOOTSTRAP_SERVER_RUNNING, KAFKA_GROUP_ID, EVENTTYPE_MATCH_FINISHED
from kafka_handler.serializers import MatchEvent
from services.ranking_service import calculate_player_ranking

class KafkaConsumerHandler:
    def __init__(self, topics, app_context):
        self.consumer = self._create_consumer(topics)
        self.app_context = app_context

    def _create_consumer(self, topics):
        """Private method to create and configure the Kafka consumer."""
        consumer = Consumer({
            'bootstrap.servers': BOOTSTRAP_SERVER_RUNNING,
            'group.id': KAFKA_GROUP_ID,
            'auto.offset.reset': 'earliest',
            'security.protocol': 'PLAINTEXT',
            # 'metadata.broker.list': BOOTSTRAP_SERVER_RUNNING,
        })
        consumer.subscribe(topics)
        return consumer

    def _process_message(self, message):
        """Private method to process a single message."""
        try:
            if not message.value():
                print("Received an empty message.")
                return
            event = MatchEvent.from_json(message.value().decode('utf-8'))
            print(f"Processing event: {event}")
            self._process_event(event)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def get_message_from_kafka(consumer, timeout=1.0):
        """ A wrapper to poll a message from Kafka """
        return consumer.poll(timeout=timeout)

    def handle_match_finished_event(self, match_id):
        print(f"Processing match ID: {match_id}", "End of the event handler chain!!!")
        # calculate_player_ranking(match_id)

    def _process_event(self, event: MatchEvent):
        if event.event_type == EVENTTYPE_MATCH_FINISHED:
            # print(event.data['match_id'])
            print(f"Handling match finished event for match_id: {event.data['match_id']}")
            self.handle_match_finished_event(event.data['match_id'])

    def consume_loop(self):
        try:
            while True:
                message = self.get_message_from_kafka(self.consumer)
                if message is None:
                    continue

                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        print(f"End of partition reached {message.topic()} [{message.partition()}] at offset {message.offset()}")
                        continue
                    else:
                        print(f"Error: {message.error()}")
                        break
                else:
                    with self.app_context:
                        self._process_message(message)
        finally:
            self.consumer.close()

    def start(self):
        consumer_tread = threading.Thread(target=self.consume_loop)
        consumer_tread.deamon = True
        consumer_tread.start()