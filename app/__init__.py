from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from .models.models import User  # Ensure models are imported here

    with app.app_context():
        db.create_all()  # Creates all tables based on models if they don't exist

    from .routes import main

    app.register_blueprint(main)

    return app
