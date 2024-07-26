from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Import the views, controllers, and models to register them with the app
from app import controller, view, model