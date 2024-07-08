import re

import requests
from bs4 import BeautifulSoup

from app.models.models import Feature, Product
from app.models.update_or_create_product import update_or_create_product
from app.scrapers.utils import (
    get_install_info,
    get_model_name,
    get_product_detail,
    get_release_year,
    get_reviews,
    get_small_img,
    get_tv_type,
    no_byme,
)

# from app import create_app, db


def scrape_data():
    worth = True
    page = 0
    listSize = 100
    out_of_stock_count = 0

    # app = create_app()

    # with app.app_context():
    while worth:
        page += 1
        if page > 9:
            break

        url = f"https://www.coupang.com/np/search?rocketAll=true&q=tv&brand=6231%2C258%2C259%2C50444%2C3143%2C53215%2C49912%2C40385%2C46698%2C17260%2C75039%2C49609%2C72371%2C56188%2C19476%2C106528%2C3154%2C75097%2C17437%2C19237&filterType=rocket%2Crocket_luxury%2Crocket_wow%2Ccoupang_global&isPriceRange=true&priceRange=100000&minPrice=100000&maxPrice=2147483647&sorter=saleCountDesc&listSize={listSize}&page={page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            product_list = soup.find(
                "ul",
                id="productList",
            ).find_all(
                "li",
                class_="search-product",
            )

            for product in product_list:
                out_of_stock = product.find("div", class_="out-of-stock")
                if out_of_stock:
                    out_of_stock_count += 1
                    if out_of_stock_count > 9:
                        worth = False
                        break
                    continue

                name = product.find("div", class_="name").text.strip()
                model_name = get_model_name(name)
                install_info = get_install_info(name)
                tv_type = get_tv_type(name)
                product_pic_s = get_small_img(product)
                rating, rating_count = get_reviews(product)

                if model_name == "no model name":
                    print("no model name: ", name)
                    continue

                if no_byme.search(name):
                    print("no byme: ", name)
                    continue

                (
                    original_price,
                    sale_price,
                    coupon_price,
                    brand,
                    product_url,
                    short_name,
                    highest_price,
                    lowest_price,
                    discount_rate,
                ) = get_product_detail(product)

                if highest_price == 0:
                    continue

                product_data = {
                    "name": name,
                    "short_name": short_name,
                    "model_name": model_name,
                    "install_info": install_info,
                    "tv_type": tv_type,
                    "product_pic_s": product_pic_s,
                    "rating": rating,
                    "rating_count": rating_count,
                    "original_price": original_price,
                    "sale_price": sale_price,
                    "coupon_price": coupon_price,
                    "highest_price": highest_price,
                    "lowest_price": lowest_price,
                    "discount_rate": discount_rate,
                    "brand": brand,
                    "product_url": product_url,
                }

                update_or_create_product(product_data)

                if out_of_stock_count != 0:
                    out_of_stock_count = 0
        else:
            print(f"Failed to retrieve page {page}")
            worth = False
