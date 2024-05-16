import os
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


def rocket_check():
    # Wait for the first checkbox input within the div to be present and clickable
    div_element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".ant-col.delivery-filter.ant-col-xs-24.ant-col-sm-12.ant-col-md-12.ant-col-lg-12",
            )
        )
    )

    # Find the first label element within the div
    first_label = div_element.find_element(By.TAG_NAME, "label")

    # Find the input checkbox within the label
    checkbox = first_label.find_element(By.TAG_NAME, "input")

    # Click the checkbox
    checkbox.click()


def get_items():
    product_list = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located(
            (
                By.CLASS_NAME,
                "product-list",
            )
        )
    )
    product_items = product_list.find_elements(By.CLASS_NAME, "product-item")
    # for item in product_items:
    #     print(item.text)
    return product_items


# Set up Chrome options for headless mode
chrome_options = Options()

# # For headless mode
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_experimental_option(
#     "prefs", {"profile.default_content_setting_values.popups": 1}
# )

# Initialize undetected-chromedriver
driver = uc.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Example of navigating to a website
driver.get("https://partners.coupang.com/#affiliate/ws/link/0/tv")
actions = ActionChains(driver)

login_coupang()

rocket_check()

items = get_items()
for item in items:
    ### info ###
    actions.move_to_element(item).perform()
    # Find the '상품정보' button within the current item context
    product_info_button = item.find_element(By.CSS_SELECTOR, "button.btn-open-detail")

    # Wait for the '상품정보' button to be clickable
    wait.until(EC.element_to_be_clickable(product_info_button))

    # Click the '상품정보' button
    product_info_button.click()

    wait.until(EC.number_of_windows_to_be(2))
    window_handles = driver.window_handles
    main_handle = window_handles[0]
    info_handle = window_handles[1]
    driver.switch_to.window(info_handle)
    ## get data from coupang

    # Close the new tab and switch back to the main tab
    driver.close()
    driver.switch_to.window(main_handle)

    ### link ###
    actions.move_to_element(item).perform()
    # Find the '링크생성' button within the current item context
    product_link_button = item.find_element(By.CSS_SELECTOR, "button.btn-generate-link")

    # Wait for the '상품정보' button to be clickable
    wait.until(EC.element_to_be_clickable(product_link_button))

    # Click the '상품정보' button
    # product_link_button.click()
    # Assuming the button doesn't have a URL attribute, use JavaScript to open in a new tab
    driver.execute_script("window.open(arguments[0].click())", product_link_button)

    wait.until(EC.number_of_windows_to_be(2))
    window_handles = driver.window_handles
    main_handle = window_handles[0]
    info_handle = window_handles[1]
    driver.switch_to.window(info_handle)

    ## get link ##
    promo_url = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".unselectable-input.shorten-url-input.large")
        )
    )
    promo_url = promo_url.text.strip()
    print(promo_url)

    # Close the new tab and switch back to the main tab
    driver.close()
    driver.switch_to.window(main_handle)


driver.quit()

# End measuring time
end_time = time.time()

# Calculate and print the total running time
total_time = end_time - start_time
print(f"Total running time: {total_time} seconds")
