from flask import Flask
from utils.db import db, DB_NAME
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

# Initialize the Flask application

def create_app(config_name=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']= "milanesa"

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for tests
        app.config['TESTING'] = True

    from .controller import ranking_controller

    app.register_blueprint(ranking_controller, url_prefix="/")

    db.init_app(app)
    migrate = Migrate(app, db)  # Set up Flask-Migrate

    return app

# Import the views, controllers, and models to register them with the app

def create_database(app):
    if not path.exists(path.join('/', DB_NAME)):  # This line is questionable
        with app.app_context():
            db.create_all()
        print('Created Database!')