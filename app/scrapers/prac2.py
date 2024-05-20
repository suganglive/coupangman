# import re

# import requests
# from bs4 import BeautifulSoup

# from .. import create_app, db  # Use relative import
# from ..models import Product

# app = create_app()
# app.app_context().push()

# # Define the pattern to match the model names
# pattern = re.compile(r"^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]+(-[A-Z0-9]+)?(\(.*\))?$")

# # to detect if product is self install or help install
# self_install = ["고객", "자가", "직접"]
# help_install = ["기사", "방문"]

# # to detect if product is stand or hang
# stand = "스탠드"
# hang = "벽걸이"


# def get_model_name(name):
#     """
#     function name = get_model_name
#     params =
#         div tag
#     explain = This function get model name from product title.
#         ex) PRISM 4K UHD TV, 139.7cm(55인치), PTC550UD, 스탠드형, 방문설치 -> PTC550UD
#     """
#     name_split = name.split(",")
#     for n in name_split:
#         n = n.strip()
#         if pattern.search(n):
#             model_name = n
#             break
#         else:
#             model_name = "no model name"

#     if model_name == "no model name":
#         name_split = name.split()
#         for n in name_split:
#             n = n.strip()
#             if pattern.search(n):
#                 model_name = n
#                 if len(model_name) < 3:
#                     continue
#                 break
#             else:
#                 model_name = "no model name"
#     return model_name


# def get_install_info(name):
#     """
#     function name = get_install_info
#     params =
#         div tag
#     explain = This function get install info name from product title.
#         ex) PRISM 4K UHD TV, 139.7cm(55인치), PTC550UD, 스탠드형, 방문설치 -> 방문설치
#     """
#     for word in self_install:
#         if word in name:
#             install = "직접설치"
#             break
#         else:
#             install = "no info"
#     if install == "no info":
#         for word in help_install:
#             if word in name:
#                 install = "방문설치"
#                 break
#             else:
#                 install = "no info"
#     return install


# def get_tv_type(name):
#     """
#     function name = get_tv_type
#     params =
#         div tag
#     explain = This function get tv type(stand or hang) name from product title.
#         ex) PRISM 4K UHD TV, 139.7cm(55인치), PTC550UD, 스탠드형, 방문설치 -> 스탠드형
#     """
#     if "스탠드" in name:
#         tv_type = "스탠드"
#     else:
#         tv_type = "no info"

#     if tv_type == "no info":
#         if "벽걸이" in name:
#             tv_type = "벽걸이"
#         else:
#             tv_type = "no info"
#     return tv_type


# def get_small_img(product):
#     """
#     function name = get_small_img
#     params =
#         li tag(product whole)
#     explain = This function get small product image. It used on main page which list products.
#         ex) //thumbnail7.coupangcdn.com/thumbnails/remote/230x230ex/image/retail/images/4121978520610508-2cea7dff-6a0d-4b8a-b379-0799ebff1e3f.jpg
#     when using img, first // is not needed.
#     """
#     img_tag = product.find("img")
#     if img_tag and "data-img-src" in img_tag.attrs:
#         product_pic_s = img_tag["data-img-src"]
#     elif (img_tag and "src" in img_tag.attrs) and (
#         img_tag and "data-img-src" not in img_tag.attrs
#     ):
#         product_pic_s = img_tag["src"]
#     else:
#         product_pic_s = "no good here"
#     return product_pic_s


# def get_reviews(product):
#     """
#     function name = get_reviews
#     params =
#         li tag(product whole)
#     explain = This function get review rating and total count of reviews.
#     """
#     review = product.find("div", class_="rating-star")
#     if review:
#         rating = review.find("span").text.strip()
#         count = review.find("span", class_="rating-total-count").text.strip()
#     else:
#         rating, count = "no review", "no review"
#     return rating, count


# def get_product_detail(product):
#     """
#     function name = get_product_detail
#     params =
#         li tag(product whole)
#     explain = This function get into product detail page, and get original, sale, coupon price, brand name, detail page url, product name(simple version).
#     all values might be not exist. if so, 'no smth' is the default value.
#     """
#     product_url = product.find("a")["href"]
#     product_url = "https://www.coupang.com/" + product_url
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#         "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
#     }

#     res = requests.get(product_url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(res.content, "html.parser")
#         original_price = soup.find("div", class_="prod-origin-price")
#         sale_price = soup.find("div", class_="prod-sale-price")
#         coupon_price = soup.find("div", class_="prod-coupon-price")

#         if original_price:
#             original_price = original_price.find(
#                 "span", class_="origin-price"
#             ).text.strip()
#         else:
#             original_price = "no original price"

#         if sale_price:
#             sale_price = sale_price.span.text.strip()
#         else:
#             sale_price = "no sale price"

#         if coupon_price:
#             coupon_price = coupon_price.span.text.strip()
#         else:
#             coupon_price = "no coupon price"

#         brand = soup.find("a", class_="prod-brand-name")
#         if brand:
#             brand = brand.text.strip()
#             if len(brand) < 1:
#                 brand = "중소기업"
#         else:
#             brand = "중소기업"

#         short_name = soup.find("h2", class_="prod-buy-header__title")
#         if short_name:
#             short_name = short_name.text.strip()
#         else:
#             short_name = "no short name"

#     return original_price, sale_price, coupon_price, brand, product_url, short_name


# url = "https://www.coupang.com/np/search?q=tv"

# # Define a custom User-Agent, Accept-Language. no Accept-Language no function
# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
# }

# # Make a GET request to the URL with the custom User-Agent
# response = requests.get(url, headers=headers)

# if response.status_code == 200:

#     soup = BeautifulSoup(response.content, "html.parser")

#     # Ensure we get the product list correctly
#     product_list = soup.find("ul", id="productList").find_all(
#         "li", class_="search-product"
#     )

#     # for loop for each product in the list.
#     for product in product_list:
#         name = product.find("div", class_="name").text.strip()
#         # get infos that access positive at list page.
#         model_name = get_model_name(name)
#         install_info = get_install_info(name)
#         tv_type = get_tv_type(name)
#         product_pic_s = get_small_img(product)
#         rating, count = get_reviews(product)

#         ### goes to product detail page to get price and brand ###
#         original_price, sale_price, coupon_price, brand, product_url, short_name = (
#             get_product_detail(product)
#         )

#         # Save product to the database
#         new_product = Product(
#             name=name,
#             short_name=short_name,
#             model_name=model_name,
#             install_info=install_info,
#             tv_type=tv_type,
#             product_pic_s=product_pic_s,
#             rating=rating,
#             count=count,
#             original_price=original_price,
#             sale_price=sale_price,
#             coupon_price=coupon_price,
#             brand=brand,
#             product_url=product_url,
#         )

#         db.session.add(new_product)
#         db.session.commit()
