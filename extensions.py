# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()
