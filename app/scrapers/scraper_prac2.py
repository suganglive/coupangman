# scraper_prac2.py
import os
import random
import time

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .. import create_app, db
from ..models import Product


def get_filename_suffix(url):
    try:
        # Find the position of the last occurrence of '.jpg'
        jpg_pos = url.rfind(".jpg")
        if jpg_pos == -1:
            return None

        # Extract the last 12 characters before '.jpg'
        start_pos = jpg_pos - 12
        if start_pos < 0:
            start_pos = 0
        return url[start_pos:jpg_pos]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def scrape_url():
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():  # Push the application context
        # Start measuring time
        start_time = time.time()

        # Load environment variables from .env file
        load_dotenv()

        # Get ID and password from environment variables
        user_id = os.getenv("ID")
        user_password = os.getenv("PW")

        def login_coupang():
            # Login to Coupang partners
            login_input = wait.until(
                EC.presence_of_element_located((By.ID, "login-email-input"))
            )
            password_input = wait.until(
                EC.presence_of_element_located((By.ID, "login-password-input"))
            )
            submit_button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        ".login__button.login__button--submit._loginSubmitButton.login__button--submit-rds",
                    )
                )
            )

            login_input.send_keys(user_id)
            password_input.send_keys(user_password)
            submit_button.click()

        # Define a custom wait condition
        def text_is_not_none(driver, previous_url):
            condition = True
            while condition:
                element = driver.find_element(
                    By.CSS_SELECTOR, ".unselectable-input.shorten-url-input.large"
                ).get_attribute("value")

                if element == previous_url:
                    print("repeat link error. try again...")
                    time.sleep(3)
                else:
                    condition = False
            # print(element)
            return element

        def get_shorten_url(product, driver, previous_url):
            pic_s = product.product_pic_s
            pic_s = get_filename_suffix(pic_s)
            model_name = product.model_name
            url = "https://partners.coupang.com/#affiliate/ws/link/0/" + model_name
            driver.get(url)

            prod_list = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-list"))
            )
            rows = prod_list.find_elements(By.CLASS_NAME, "product-row")
            the_item = 0
            for row in rows:
                if the_item == 0:
                    items = row.find_elements(By.CLASS_NAME, "product-item")
                    for item in items:
                        img = item.find_element(By.CLASS_NAME, "product-picture")
                        img_src = img.find_element(By.TAG_NAME, "img").get_attribute(
                            "src"
                        )

                        img_src = get_filename_suffix(img_src)

                        if img_src == pic_s:
                            print(img_src, pic_s)
                            the_item = item
                            break
                else:
                    break

            # Can't found matching product.
            if the_item == 0:
                return None

            actions.move_to_element(the_item).perform()
            product_link_button = the_item.find_element(
                By.CSS_SELECTOR, "button.btn-generate-link"
            )
            wait.until(EC.element_to_be_clickable(product_link_button))
            product_link_button.click()

            # link page
            shorten_url = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".unselectable-input.shorten-url-input.large",
                    )
                )
            )
            # Wait until the text is not None
            shorten_url_text = WebDriverWait(driver, 10).until(
                text_is_not_none(driver, previous_url)
            )
            return shorten_url_text

        # Set up Chrome options for headless mode
        chrome_options = Options()

        # # For headless mode
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_experimental_option(
        #     "prefs", {"profile.default_content_setting_values.popups": 1}
        # )

        # Initialize undetected-chromedriver
        driver = uc.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 100)

        # Example of navigating to a website
        url = "https://partners.coupang.com/#affiliate/ws/link/0/"
        driver.get(url)
        actions = ActionChains(driver)

        login_coupang()
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-input.ant-input-lg"))
        )
        # Retrieve all model names from the database
        # model_names = [product.model_name for product in Product.query.all()]
        products = Product.query.all()

        previous_url = 0

        for i in range(1, len(products) + 1):
            try:
                the_product = products[i - 1]
                the_product.shorten_url = None

                shorten_url_text = get_shorten_url(the_product, driver, previous_url)
                print(the_product.id, the_product.model_name)
                print(shorten_url_text)

                if shorten_url_text != None:
                    if shorten_url_text == previous_url:
                        while shorten_url_text == previous_url:
                            print(
                                f"same url error. do again product id: {the_product.id}"
                            )
                            # refresh
                            url = "https://partners.coupang.com/#affiliate/ws/link/0/tv"
                            driver.get(url)

                            time.sleep(random.uniform(8, 10))

                            shorten_url_text = get_shorten_url(
                                the_product, driver, previous_url
                            )

                            print(the_product.id, the_product.model_name)
                            print(shorten_url_text)

                # Introduce a random delay between 1 and 3 seconds
                time.sleep(random.uniform(8, 10))

                # Update the Product with the shorten_url
                if the_product:
                    the_product.shorten_url = shorten_url_text
                    db.session.commit()
                    previous_url = shorten_url_text
            except Exception as e:
                print(f"Error processing model {i}: {e}")
                continue
        driver.quit()

        # End measuring time
        end_time = time.time()

        # Calculate and print the total running time
        total_time = end_time - start_time
        print(f"Total running time: {total_time} seconds")