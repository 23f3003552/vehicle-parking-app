from flask import Flask, redirect, url_for, render_template
from config import Config
from extensions import db, migrate
from controllers.auth import auth
from models import *  # Ensure models are imported so Alembic can detect them

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration (e.g., DB URI, SECRET_KEY)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/auth")  # Add a prefix for clarity

@app.route("/")
def test():
    return "<h1>text</h1>"

if __name__ == "__main__":
    app.run(debug=True)
