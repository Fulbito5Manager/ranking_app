from flask import Flask
from services.kafka_consumer import start_kafka_consumer
from app import create_app
import threading

app = create_app()

def run_kafka_consumer():
    start_kafka_consumer()

if __name__ == '__main__':
    # Start Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=run_kafka_consumer)
    consumer_thread.start()
    
    # Run Flask app
    app.run(debug=True)
