from celery.schedules import crontab


class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "sqlite:///yourdatabase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery configuration
    CELERY_BROKER_URL = "redis://svc.xxx.cloudtype.app:32146/0"
    CELERY_RESULT_BACKEND = "redis://svc.xxx.cloudtype.app:6379/0"
    CELERY_BEAT_SCHEDULE = {
        "daily-scrape-task": {
            "task": "app.tasks.total_scrape_task",
            "schedule": crontab(minute=0, hour=18),
        },
    }

    CELERY_TIMEZONE = "UTC"
