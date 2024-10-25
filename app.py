from flask import Flask
# from services.kafka_consumer import consumer
# from app.controller import ranking_controller
from app import create_app, create_database
from services.kafka_consumer import start_kafka_consumer

app = create_app()

if __name__ == '__main__':
    start_kafka_consumer()
    create_database(app)
    app.run(debug=True)