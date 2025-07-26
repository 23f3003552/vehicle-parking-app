from flask import Flask, redirect, url_for
from config import Config
from extensions import db, migrate
from controllers.auth import auth
from controllers.userdash import userdash
from models import *  # Import models so Alembic can detect them

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations (DB URI, SECRET_KEY)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(auth, url_prefix="/auth")

    # Default route
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
