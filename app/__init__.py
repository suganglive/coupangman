import re

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

    # Custom filter to match regex patterns
    def match_filter(s, pattern):
        return re.match(pattern, s) is not None

    # Custom filter to add commas as thousands separators
    def add_commas(value):
        value = int(value)
        if isinstance(value, (int, float)):
            return "{:,}".format(value)
        return value

    # Register the custom filter with Jinja
    app.jinja_env.filters["add_commas"] = add_commas
    app.jinja_env.filters["strip"] = strip_filter
    app.jinja_env.filters["truncate"] = truncate_filter
    app.jinja_env.filters["match"] = match_filter

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models

        db.create_all()  # Creates all tables based on models if they don't exist

    from .routes import main

    app.register_blueprint(main)

    return app
