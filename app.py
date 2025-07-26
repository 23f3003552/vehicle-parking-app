from flask import Flask
from config import Config
from extensions import db, migrate
from models import *   # import models so Alembic sees them

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return "OK"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)