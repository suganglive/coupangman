import re

import requests
from bs4 import BeautifulSoup

from .. import create_app, db
from ..models import Feature, Product

# Define the pattern to match the model names
pattern = re.compile(r"^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]+(-[A-Z0-9]+)?(\(.*\))?$")
no_byme = re.compile(f"\b바이미\b")

# to detect if product is self install or help install
self_install = ["고객", "자가", "직접"]
help_install = ["기사", "방문"]

# to detect if product is stand or hang
stand = "스탠드"
hang = "벽걸이"


def check_and_add_feature_name(name, prod):
    existing_feature = Feature.query.filter_by(name=name).first()
    if existing_feature:
        print(f"Feature '{name}' already exists.")
        prod.features.append(existing_feature)
    else:
        new_feature = Feature(name=name)
        db.session.add(new_feature)
        db.session.commit()
        print(f"Feature '{name}' added to the database.")
        prod.features.append(new_feature)
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
    # Create a list of prices ignoring None values
    prices = [p for p in [original_price, sale_price, coupon_price] if p is not None]

    if not prices:
        return 0, 0, 0

    # Determine the highest and lowest prices
    highest_price = max(prices)
    lowest_price = min(prices)

    # Calculate the discount rate
    if highest_price is not None and lowest_price is not None:
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

        short_name = soup.find("h2", class_="prod-buy-header__title")
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


def scrape_data():
    worth = True
    page = 0
    listSize = 100
    out_of_stock_count = 0

    app = create_app()

    with app.app_context():
        while worth:
            page += 1
            print(f"page {page} started.")
            url = f"https://www.coupang.com/np/search?rocketAll=true&q=tv&brand=6231%2C258%2C259%2C50444%2C3143%2C53215%2C49912%2C40385%2C46698%2C17260%2C75039%2C49609%2C72371%2C56188%2C19476%2C106528%2C3154%2C75097%2C17437%2C19237&filterType=rocket%2Crocket_luxury%2Crocket_wow%2Ccoupang_global&isPriceRange=true&priceRange=100000&minPrice=100000&maxPrice=2147483647&sorter=saleCountDesc&listSize={listSize}&page={page}"

            # Define a custom User-Agent, Accept-Language. no Accept-Language no function
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
            }

            # Make a GET request to the URL with the custom User-Agent
            response = requests.get(url, headers=headers)

            if response.status_code == 200:

                soup = BeautifulSoup(response.content, "html.parser")

                # Ensure we get the product list correctly
                product_list = soup.find("ul", id="productList").find_all(
                    "li", class_="search-product"
                )

                # for loop for each product in the list.
                for product in product_list:
                    # 품절일 경우 넘어감
                    out_of_stock = product.find("div", class_="out-of-stock")
                    if out_of_stock:
                        out_of_stock_count += 1
                        if out_of_stock_count > 9:
                            worth = False
                            break
                        print("no stock left for prod")
                        continue

                    # get infos that access positive at list page.
                    name = product.find("div", class_="name").text.strip()
                    model_name = get_model_name(name)
                    install_info = get_install_info(name)
                    tv_type = get_tv_type(name)
                    product_pic_s = get_small_img(product)
                    rating, count = get_reviews(product)

                    # skip no model name.
                    if model_name == "no model name":
                        print("no no model name: ", name)
                        continue

                    # 바이미 스킵
                    is_it_byme = no_byme.search(name)
                    if is_it_byme:
                        print("no byme: ", name)
                        continue

                    ### goes to product detail page to get price and brand ###
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

                    # 가격 정보중 최고가가 0인 경우 넘어감.
                    if highest_price == 0:
                        continue

                    release = get_release_year(model_name)

                    # Save product to the database
                    new_product = Product(
                        name=name,
                        short_name=short_name,
                        model_name=model_name,
                        install_info=install_info,
                        tv_type=tv_type,
                        product_pic_s=product_pic_s,
                        rating=rating,
                        count=count,
                        original_price=original_price,
                        sale_price=sale_price,
                        coupon_price=coupon_price,
                        highest_price=highest_price,
                        lowest_price=lowest_price,
                        discount_rate=discount_rate,
                        brand=brand,
                        product_url=product_url,
                        release=release,
                    )

                    db.session.add(new_product)
                    db.session.commit()

                    if out_of_stock_count != 0:
                        out_of_stock_count = 0
