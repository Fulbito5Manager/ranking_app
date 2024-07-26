from flask import Flask
# from services.kafka_consumer import consumer

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Ranking System"

if __name__ == '__main__':
    app.run(debug=True)