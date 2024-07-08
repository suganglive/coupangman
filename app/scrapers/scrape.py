from app import create_app
from app.scrapers.scraper_basic import scrape_data
from app.scrapers.scraper_feature import scrape_features
from app.scrapers.scraper_url import scrape_url


def total_scrape():
    app = create_app()

    with app.app_context():
        scrape_data()
        scrape_url()
        scrape_features()


if __name__ == "__main__":
    total_scrape()
