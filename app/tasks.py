# from app import create_app, db, make_celery
from app import app, celery

# from .celery import celery_app
from app.models.update_or_create_product import delete_old_products, isit_best_offer
from app.scrapers.scraper_basic import scrape_data
from app.scrapers.scraper_feature import scrape_features
from app.scrapers.scraper_url import scrape_url
from app.scrapers.scraper_url2 import scrape_url2

# app = create_app()
# celery = make_celery(app)


@celery.task
def scrape_data_task():
    with app.app_context():
        scrape_data()


@celery.task
def scrape_features_task():
    with app.app_context():
        scrape_features()


@celery.task
def scrape_url_task():
    with app.app_context():
        scrape_url()


@celery.task
def scrape_url_task2():
    with app.app_context():
        scrape_url2()


@celery.task
def best_offer_task():
    with app.app_context():
        isit_best_offer()

@celery.task
def delete_old_products_task():
    with app.app_context():
        delete_old_products()


@celery.task
def total_scrape_task():
    with app.app_context():
        scrape_data()
        print("1 end")
        scrape_url2()
        print("2 end")
        scrape_features()
        print("3 end")
        delete_old_products()
        print("4 end")
        isit_best_offer()
        print("5 end")
