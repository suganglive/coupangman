import re

import requests
from bs4 import BeautifulSoup

# Define the pattern to match the model names

# pattern = re.compile(r"\b^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]+(-[A-Z0-9]+)?(\(.*\))?$\b")
pattern = re.compile(r"^(?=.*[A-Z])(?=.*[0-9])[A-Z0-9]+(-[A-Z0-9]+)?(\(.*\))?$")
self_install = ["고객", "자가", "직접"]
help_install = ["기사", "방문"]
stand = "스탠드"
hang = "벽걸이"


url = "https://www.coupang.com/np/search?q=tv"

# Define a custom User-Agent
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
}

# Make a GET request to the URL with the custom User-Agent
response = requests.get(url, headers=headers)

# Print the status code of the response
print(f"Status Code: {response.status_code}")

soup = BeautifulSoup(response.content, "html.parser")

# Ensure we get the product list correctly
product_list = soup.find("ul", id="productList").find_all("li", class_="search-product")

for product in product_list:
    name = product.find("div", class_="name").text.strip()
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

    if "스탠드" in name:
        tv_type = "스탠드"
    else:
        tv_type = "no info"

    if tv_type == "no info":
        if "벽걸이" in name:
            tv_type = "벽걸이"
        else:
            tv_type = "no info"

    print(name)
    print(model_name)
    print(install)
    print(tv_type)
    print("\n")

# 고객, 자가, 직접 // 방문, 기사 // 스탠드 // 벽걸이 //
