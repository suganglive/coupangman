import re

from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.config_from_object("app.config.Config")  # Correct the import path
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Correct the import path

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

    # Ensure models are imported to initialize tables
    with app.app_context():
        from .models import models  # Ensure this is imported

        db.create_all()  # Creates all tables based on models if they don't exist

    from .routes import main

    app.register_blueprint(main)

    # Flag to ensure the scraper runs only once
    app.scraper_ran = False

    # Create the Celery instance
    celery = make_celery(app)
    app.celery = celery

    return app


# Initialize the app and celery instances
app = create_app()
celery = app.celery
