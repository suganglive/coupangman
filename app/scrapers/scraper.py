import os
import time

from dotenv import load_dotenv
from fake_useragent import UserAgent
from pynput import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Load environment variables from .env file
load_dotenv()

# Get ID and password from environment variables
user_id = os.getenv("ID")
user_password = os.getenv("PW")


# def on_press(key):
#     try:
#         if key == keyboard.Key.space:  # Check if the spacebar is pressed
#             print("Spacebar pressed! Starting actions...")
#             start_actions()
#             return False  # Stop listener after action starts
#     except AttributeError:
#         print(f"Special key pressed: {key}")


def start_actions():
    try:
        # Login to Coupang partners
        login_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-email-input"))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-password-input"))
        )
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".login__button.login__button--submit._loginSubmitButton.login__button--submit-rds",
                )
            )
        )

        # Debugging: print the placeholder text to verify element access
        print(f"Email placeholder: {login_input.get_attribute('placeholder')}")
        print(f"Password placeholder: {password_input.get_attribute('placeholder')}")

        login_input.send_keys(user_id)
        password_input.send_keys(user_password)
        submit_button.click()

        # Locate the checkbox element using its class name and check it
        checkbox = driver.find_element(By.CLASS_NAME, "ant-checkbox-input")

        # Check if the checkbox is not already checked and then click it
        if not checkbox.is_selected():
            checkbox.click()

        time.sleep(100)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(driver.page_source)


# Setup options for Chrome to make Selenium less detectable
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
user_ag = UserAgent().random
options.add_argument(f"user-agent={user_ag}")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2}
)

# Additional performance-related options
options.add_argument("--headless")  # Run in headless mode for faster performance
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")

# # Specify the path to your custom ChromeDriver
# service = Service(
#     "/Users/sugang/Documents/GitHub/coupangman/app/scrapers/chromedriver/chromedriver-mac-arm64/chromedriver"
# )

driver = webdriver.Chrome(options=options)

# Modify the browser's navigator.webdriver property
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    },
)

# Open the Coupang login page
driver.get("https://partners.coupang.com/#affiliate/ws/link/0/tv")

# Wait for the spacebar press
print("Press the spacebar to start actions.")
start_actions
# with keyboard.Listener(on_press=on_press) as listener:
#     listener.join()

# Close the browser
driver.quit()
