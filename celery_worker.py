# import app.models.isit_best_offer
import app.models.update_or_create_product
import app.scrapers.scraper_basic
import app.scrapers.scraper_feature
import app.scrapers.scraper_url
import app.scrapers.scraper_url2

# Ensure that tasks are imported
import app.tasks
from app import app, celery
