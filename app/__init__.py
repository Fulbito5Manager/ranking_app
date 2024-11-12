from flask import Flask
from utils.db import db, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from settings import Config, TestConfig

# Initialize the Flask application

def create_app(config_name=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY']= Config.SECRET_KEY

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = TestConfig.TESTING_SQLALCHEMY_DATABASE_URI
        app.config['TESTING'] = TestConfig.TESTING
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TestConfig.TESTING_SQLALCHEMY_TRACK_MODIFICATIONS

    from .controller import ranking_controller

    app.register_blueprint(ranking_controller, url_prefix="/")

    db.init_app(app)
    migrate.init_app(app, db)  # Set up Flask-Migrate

    return app

# def create_database(app):
#     with app.app_context():
#         db.create_all()  # Re-create tables after dropping them
#     # print('Dropped and Created Database!')