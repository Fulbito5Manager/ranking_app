from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
DB_NAME = 'database.db'

migrate = Migrate()
