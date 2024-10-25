KAFKA_BOOTSTRAP_SERVERS = '#'
PLAYER_SERVICE_URL = 'http://localhost:8082'
MATCH_SERVICE_URL = 'http://localhost:8080'  # CHANGE
# USER_SERVICE_TOKEN
# USER_SERVICE_PASSWORD

BOOTSTRAP_SERVER_RUNNING = 'localhost:9092'
KAFKA_GROUP_ID = 'ranking-group'

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = 'milanesa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Other config options

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False