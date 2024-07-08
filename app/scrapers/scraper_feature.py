import pprint
import re
import time
from datetime import date

import requests
from bs4 import BeautifulSoup

from app import create_app, db
from app.models.models import Feature, Product
from app.scrapers.utils import check_and_add_feature_name, codes, extract_screen_size


def scrape_features():
    # Create the Flask application
    # app = create_app()

    # Run the code within the application context
    # with app.app_context():
    # Query all products
    basic_url = "https://search.danawa.com/dsearch.php?tab=main&query="
    products = Product.query.all()

    for product in products:
        # Skip products whose features have already been scraped
        if product.features_scraped:
            print(
                f"Features for product {product.model_name} already scraped. Skipping."
            )
            continue
        model_brand = product.brand
        model_name = product.model_name
        shorten_url = product.shorten_url

        if shorten_url is None:
            print("No link no money")
            continue

        if model_brand != "중소기업":
            url = basic_url + model_brand + "+" + model_name
        else:
            url = basic_url + model_name

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")

        items = soup.find("ul", class_="product_list")
        if items:
            items = items.find_all("li")
        else:
            continue
        for item in items:
            temp = item.find("dl", class_="prod_category_location")
            if temp:
                temp = temp.find("span")
                if temp:
                    temp = temp.text.strip()
                    if temp == "TV":
                        break
        spec_list = item.find("div", class_="spec_list")
        if spec_list:
            spec_list = spec_list.text
            spec_list = spec_list.split("/")
            clean_spec_list = [
                spec.strip().replace("\t", "").replace("\n", "") for spec in spec_list
            ]
            # Initialize the dictionary
            dic = {
                "기본": {
                    "screen_size": "",
                    "display_tech": "",
                    "resolution": "",
                    "refresh_rate": "",
                },
                "화질": {},
                "사운드": {},
                "스마트": {},
                "부가": {},
                "보증기간": {},
                "게임": {},
            }

            # Populate the dictionary
            current_category = "기본"
            for spec in clean_spec_list:
                if "[화질]" in spec:
                    current_category = "화질"
                elif "[게임]" in spec:
                    current_category = "게임"
                elif "[스마트]" in spec:
                    current_category = "스마트"
                    dic[current_category][spec.replace("[스마트] ", "")] = True
                elif "[사운드]" in spec:
                    current_category = "사운드"
                elif "[부가]" in spec:
                    current_category = "부가"
                elif "[보증기간]" in spec:
                    current_category = "보증기간"

                if current_category == "기본":
                    if "인치" in spec:
                        dic["기본"]["screen_size"] = extract_screen_size(spec)
                    elif spec.endswith("ED"):
                        dic["기본"]["display_tech"] = spec
                    elif spec.endswith("HD"):
                        dic["기본"]["resolution"] = spec
                    elif "주사율" in spec:
                        dic["기본"]["refresh_rate"] = spec.split(": ")[1]

                else:
                    if "]" in spec:
                        spec = spec.split("]")[1].strip()
                    if ":" in spec:
                        spec_split = spec.split(":")
                        k = spec_split[0].strip()
                        v = spec_split[1].strip()
                        if v == "X":
                            continue
                        dic[current_category][k] = v
                        continue

                    if len(spec) > 20:
                        continue
                    dic[current_category][spec] = True

            print(f"model name : {model_name}\n spec list: {clean_spec_list}")
            del dic["보증기간"]

            for cat in dic:
                for feature in dic[cat]:
                    if feature == "크기(가로x세로x깊이)":
                        continue
                    code = codes[cat]
                    check_and_add_feature_name(
                        name=feature,
                        value=dic[cat][feature],
                        feature_code=code,
                        prod=product,
                    )

            # Mark the product's features as scraped
            product.features_scraped = True
            db.session.commit()

            time.sleep(2)
        else:
            print(f"model name : {model_name}\n spec list: has no spec_list")
