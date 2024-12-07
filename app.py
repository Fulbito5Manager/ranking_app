from flask import Flask
from kafka_handler.kafka_consumer import start_kafka_consumer
from app import create_app
import threading
from kafka_handler import KafkaConsumerHandler

app = create_app()

# def start_kafka_consumer():
#     topics = ['match_service_topic']
#     consumer.subscribe(topics)
#     consumer_thread = threading.Thread(target=consume_loop)
#     consumer_thread.daemon = True  # Para que se cierre cuando la app Flask se cierre
#     consumer_thread.start()

def start_kafka_consumer():
    topics = ['match_service_topic']
    kafka_handler = KafkaConsumerHandler(topics, app.app_context())
    kafka_handler.start()

if __name__ == '__main__':
    app = create_app()
    start_kafka_consumer()
    app.run(debug=True)
