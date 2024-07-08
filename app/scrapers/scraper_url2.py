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

from app import create_app, db
from app.models.models import Product
from app.scrapers.utils import get_filename_suffix


def scrape_url2():
    # app = create_app()  # Create an instance of your Flask app
    # with app.app_context():  # Push the application context
    # Start measuring time
    start_time = time.time()

    # Load environment variables from .env file
    load_dotenv()

    # Get ID and password from environment variables
    user_id = os.getenv("ID")
    user_password = os.getenv("PW")

    # Function to handle the modal
    def handle_modal():
        try:
            modal_present = driver.find_element(By.CLASS_NAME, "ant-modal-content")
            if modal_present:
                password_input = driver.find_element(By.ID, "password")
                password_input.send_keys(user_password)
                confirm_button = driver.find_element(
                    By.XPATH, "//button[@type='submit']"
                )
                confirm_button.click()
                # Wait until modal disappears
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located(
                        (By.CLASS_NAME, "ant-modal-content")
                    )
                )
                print("modal handled@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        except Exception as e:
            # print("No modal present or error handling modal")
            pass

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
    def text_is_not_none(driver):
        shorten_url = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".unselectable-input.tracking-url-input.large",
                )
            )
        )
        condition = True
        while condition:
            element = driver.find_element(
                By.CSS_SELECTOR, ".unselectable-input.tracking-url-input.large"
            ).text.strip()

            # print(f"current url = {element}, previous url = {previous_url}")
            if element == previous_url:
                handle_modal()
                print("repeat link error. try again...")
                time.sleep(3)
            else:
                condition = False

        return element

    def get_shorten_url(product, driver):
        # print(product.model_name, product.id)
        url = product.product_url
        # Locate the input element using its class name and id
        input_element = wait.until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "url",
                )
            )
        )
        submit_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".ant-btn.lg.ant-btn-primary",
                )
            )
        )
        # Clear the existing value if needed
        input_element.clear()
        input_element.send_keys(url)
        submit_button.click()
        handle_modal()
        # time.sleep(2)

        try:
            # # Wait until the text is not None
            shorten_url_text = WebDriverWait(driver, 10).until(text_is_not_none)

            # print(shorten_url_text)

        except:
            handle_modal()
            print(f"found image but no actions perfome? why?")
            return None

        return shorten_url_text

    # Set up Chrome options for headless mode
    chrome_options = Options()

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize undetected-chromedriver
    driver = uc.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 100)

    # Example of navigating to a website
    url = "https://partners.coupang.com/#affiliate/ws/link-to-any-page"
    driver.get(url)
    # actions = ActionChains(driver)

    login_coupang()
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-input.ant-input-lg"))
    )
    # Retrieve all model names from the database
    # model_names = [product.model_name for product in Product.query.all()]
    products = Product.query.all()

    previous_url = None

    for i in range(1, len(products) + 1):
        try:
            the_product = products[i - 1]
            # the_product.shorten_url = None

            print(the_product.id, the_product.model_name)
            if the_product.shorten_url:
                print(
                    f"{the_product.model_name} already got shorten_url: {the_product.shorten_url}"
                )
                continue
            else:
                handle_modal()
                shorten_url_text = get_shorten_url(the_product, driver)
            # handle_modal()
            # shorten_url_text = get_shorten_url(the_product, driver)

            # Introduce a random delay between 1 and 3 seconds
            time.sleep(random.uniform(1, 3))

            # Update the Product with the shorten_url
            if the_product:
                the_product.shorten_url = shorten_url_text
                db.session.commit()
                if shorten_url_text != None:
                    previous_url = shorten_url_text

        except Exception as e:
            handle_modal()
            print(f"Error processing model {i}: {e}")
            continue
    driver.quit()

    # End measuring time
    end_time = time.time()

    # Calculate and print the total running time
    total_time = end_time - start_time
    print(f"Total running time: {total_time} seconds")
