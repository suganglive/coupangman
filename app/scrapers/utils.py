import re

import requests
from bs4 import BeautifulSoup

from app import db
from app.models.models import Feature, Product

# Define the pattern to match the model names
pattern = re.compile(r"^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]+(-[A-Z0-9]+)?(\(.*\))?$")
pattern2 = re.compile(
    r"\b[A-Za-z]{1,2}\d{2,}([A-Za-z0-9]*[A-Za-z]{1,2}[A-Za-z0-9]*)?\b"
)
size_pattern = re.compile(r"[0-9]{2,3}인치")
size2_pattern = re.compile(r"[0-9]+")

no_byme = re.compile(f"\b바이미\b")

# to detect if product is self install or help install
self_install = ["고객", "자가", "직접"]
help_install = ["기사", "방문"]

# to detect if product is stand or hang
stand = "스탠드"
hang = "벽걸이"

codes = {"기본": 1, "화질": 2, "사운드": 3, "스마트": 4, "게임": 5, "부가": 6}


def get_filename_suffix(url):
    try:
        # Find the position of the last occurrence of '.'
        jpg_pos = url.rfind(".")
        if jpg_pos == -1:
            return None

        # Extract the last 12 characters before '.'
        start_pos = jpg_pos - 12
        if start_pos < 0:
            start_pos = 0
        return url[start_pos:jpg_pos]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Helper function to extract screen size
def extract_screen_size(text):
    return text.split("(")[0]


def check_and_add_feature_name(name, feature_code, value, prod):
    # Check if the feature already exists
    existing_feature = Feature.query.filter_by(name=name, value=value).first()

    if existing_feature:
        print(f"Feature name: '{name}', value: '{value}' already exists.")

        # Check if the product already has this feature
        if existing_feature not in prod.features:
            prod.features.append(existing_feature)
    else:
        # Create a new feature if it doesn't exist
        new_feature = Feature(name=name, value=value, feature_code=feature_code)
        db.session.add(new_feature)
        db.session.commit()
        print(f"Feature '{name}', value: '{value}' added to the database.")
        prod.features.append(new_feature)

    # Commit the changes to the database
    db.session.commit()


def get_danawa(model_name):
    url = "https://search.danawa.com/dsearch.php?query=" + model_name
    # Define a custom User-Agent, Accept-Language. no Accept-Language no function

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup


def get_release_year(model_name):
    if model_name == "no model name":
        return "no release info"
    soup = get_danawa(model_name)
    mt_date = soup.find("dl", class_="meta_item mt_date")
    if mt_date:
        release = mt_date.find("dd").text.strip()
    else:
        release = "no release info"
    return release


def get_prod_tags(model_name):
    soup = get_danawa(model_name)
    first_item = soup.find("ul", class_="product_list").find("li")
    spec_list = first_item.find("div", class_="spec_list")
    # if spec_list and len(spec_list.get("class", [])) < 2:
    size, panel, resolution = None, None, None  # Initialize variables
    if spec_list:
        for idx, i in enumerate(spec_list.children):

            try:
                if idx == 3:
                    size = i.text.strip()
                if idx == 5:
                    panel = i.text.strip()
                if idx == 7:
                    resolution = i.text.strip()
                    break
            except:
                pass
        print(model_name)
        return size, panel, resolution
    else:
        print(model_name)
        return size, panel, resolution


def get_only_numbers(string):
    if string:
        string = string.replace("원", "")
        string = string.replace(",", "")
        string = int(string)

    return string


def get_high_low_discount(original_price, sale_price, coupon_price):
    highest_price = 0
    lowest_price = 0

    if original_price and sale_price and coupon_price:
        highest_price = original_price
        lowest_price = coupon_price

    if not original_price and sale_price and coupon_price:
        highest_price = sale_price
        lowest_price = coupon_price
    if original_price and not sale_price and coupon_price:
        highest_price = original_price
        lowest_price = coupon_price
    if not original_price and not sale_price and coupon_price:
        highest_price = coupon_price
        lowest_price = coupon_price

    if original_price and not sale_price and coupon_price:
        highest_price = original_price
        lowest_price = coupon_price
    if original_price and sale_price and not coupon_price:
        highest_price = original_price
        lowest_price = sale_price
    if original_price and not sale_price and not coupon_price:
        highest_price = original_price
        lowest_price = original_price

    if not original_price and sale_price and not coupon_price:
        highest_price = sale_price
        lowest_price = sale_price
    if not original_price and sale_price and coupon_price:
        highest_price = sale_price
        lowest_price = coupon_price
    if original_price and sale_price and not coupon_price:
        highest_price = original_price
        lowest_price = sale_price

    if highest_price != 0 and lowest_price != 0:
        discount_rate = ((highest_price - lowest_price) / highest_price) * 100
        discount_rate = round(discount_rate, 2)
    else:
        discount_rate = None

    return highest_price, lowest_price, discount_rate


def get_model_name(name):
    """
    function name = get_model_name
    params =
        div tag
    explain = This function get model name from product title.
        ex) PRISM 4K UHD TV, 139.7cm(55인치), PTC550UD, 스탠드형, 방문설치 -> PTC550UD
    """
    name_split = name.split(",")
    for n in name_split:
        n = n.strip()
        if pattern.search(n):
            model_name = n
            break
        else:
            model_name = "no model name"

    if model_name == "no model name":
        name_split = name.split()
        for n in name_split:
            n = n.strip()
            if pattern.search(n):
                model_name = n
                if len(model_name) < 3:
                    continue
                break
            else:
                model_name = "no model name"

    # Check if model_name is "no model name"
    if model_name == "no model name":
        match = pattern2.search(name)
        if match:
            model_name = match.group()

    if name.startswith("TCL") and len(model_name) < 4:
        try:
            match = size_pattern.search(name)
            if match:
                size = match.group()
                if len(size) == 4:
                    size = size[:2]
                else:
                    size = size[:3]
                model_name = size + model_name
        except:
            pass

    return model_name


def get_install_info(name):
    """
    function name = get_install_info
    params =
        div tag
    explain = This function get install info name from product title.
        ex) PRISM 4K UHD TV, 139.7cm(55인치), PTC550UD, 스탠드형, 방문설치 -> 방문설치
    """
    for word in self_install:
        if word in name:
            install = "직접설치"
            break
        else:
            install = "no info"
    if install == "no info":
        for word in help_install:
            if word in name:
                install = "방문설치"
                break
            else:
                install = "no info"
    return install


def get_tv_type(name):
    """
    function name = get_tv_type
    params =
        div tag
    explain = This function get tv type(stand or hang) name from product title.
        ex) PRISM 4K UHD TV, 139.7cm(55인치), PTC550UD, 스탠드형, 방문설치 -> 스탠드형
    """
    if "스탠드" in name:
        tv_type = "스탠드"
    else:
        tv_type = "no info"

    if tv_type == "no info":
        if "벽걸이" in name:
            tv_type = "벽걸이"
        else:
            tv_type = "no info"
    return tv_type


def get_small_img(product):
    """
    function name = get_small_img
    params =
        li tag(product whole)
    explain = This function get small product image. It used on main page which list products.
        ex) //thumbnail7.coupangcdn.com/thumbnails/remote/230x230ex/image/retail/images/4121978520610508-2cea7dff-6a0d-4b8a-b379-0799ebff1e3f.jpg
    when using img, first // is not needed.
    """
    img_tag = product.find("img")
    if img_tag and "data-img-src" in img_tag.attrs:
        product_pic_s = img_tag["data-img-src"]
    elif (img_tag and "src" in img_tag.attrs) and (
        img_tag and "data-img-src" not in img_tag.attrs
    ):
        product_pic_s = img_tag["src"]
    else:
        product_pic_s = "no good here"
    product_pic_s = "https:" + product_pic_s
    return product_pic_s


def get_reviews(product):
    """
    function name = get_reviews
    params =
        li tag(product whole)
    explain = This function get review rating and total count of reviews.
    """
    review = product.find("div", class_="rating-star")
    if review:
        rating = review.find("span").text.strip()
        count = review.find("span", class_="rating-total-count").text.strip()
    else:
        rating, count = "no review", "no review"
    return rating, count


def get_product_detail(product):
    """
    function name = get_product_detail
    params =
        li tag(product whole)
    explain = This function get into product detail page, and get original, sale, coupon price, brand name, detail page url, product name(simple version).
    all values might be not exist. if so, 'no smth' is the default value.
    """
    product_url = product.find("a")["href"]
    product_url = "https://www.coupang.com/" + product_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
    }

    res = requests.get(product_url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "html.parser")
        original_price = soup.find("div", class_="prod-origin-price")
        sale_price = soup.find("div", class_="prod-sale-price")
        coupon_price = soup.find("div", class_="prod-coupon-price")

        if original_price:
            original_price = original_price.find(
                "span", class_="origin-price"
            ).text.strip()
        else:
            original_price = None
        if sale_price:
            sale_price = sale_price.span.text.strip()
        else:
            sale_price = None

        if coupon_price:
            coupon_price = coupon_price.span.text.strip()
        else:
            coupon_price = None

        original_price = get_only_numbers(original_price)
        sale_price = get_only_numbers(sale_price)
        coupon_price = get_only_numbers(coupon_price)

        highest_price, lowest_price, discount_rate = get_high_low_discount(
            original_price, sale_price, coupon_price
        )

        brand = soup.find("a", class_="prod-brand-name")
        if brand:
            brand = brand.text.strip()
            if len(brand) < 1:
                brand = "중소기업"
        else:
            brand = "중소기업"

        short_name = soup.find("h1", class_="prod-buy-header__title")
        if short_name:
            short_name = short_name.text.strip()
        else:
            short_name = "no short name"

    return (
        original_price,
        sale_price,
        coupon_price,
        brand,
        product_url,
        short_name,
        highest_price,
        lowest_price,
        discount_rate,
    )
