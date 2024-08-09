from celery.schedules import crontab


class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "sqlite:///yourdatabase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery configuration
    CELERY_BROKER_URL = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
    # CELERY_BROKER_URL = "redis://svc.sel5.cloudtype.app:32146/0"
    # CELERY_RESULT_BACKEND = "redis://redis:6379/0"
    CELERYBEAT_SCHEDULE = {
        "scheduled-task": {
            "task": "app.tasks.total_scrape_task",
            "schedule": crontab(minute=3, hour=17),
        },
    }

    CELERY_TIMEZONE = "Asia/Seoul"
