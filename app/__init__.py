from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Custom filter to strip leading and trailing whitespace
    def strip_filter(value):
        if isinstance(value, str):
            return value.strip().replace("(", "").replace(")", "")
        return value

    # Custom filter to truncate text
    def truncate_filter(value, length=30):
        if isinstance(value, str) and len(value) > length:
            return value[:length] + "..."
        return value

    app.jinja_env.filters["strip"] = strip_filter
    app.jinja_env.filters["truncate"] = truncate_filter

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models

        db.create_all()  # Creates all tables based on models if they don't exist

    from .routes import main

    app.register_blueprint(main)

    return app
