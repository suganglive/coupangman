import time

from pynput import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By


def on_press(key):
    try:
        if key == keyboard.Key.space:  # Check if the spacebar is pressed
            print("Spacebar pressed! Starting actions...")
            start_actions()
            return False  # Stop listener after action starts
    except AttributeError:
        print(f"Special key pressed: {key}")


def start_actions():
    # Add your actions here. For example, search for a term on Google.
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python")
    search_box.submit()


# Set up the WebDriver (Make sure to have the correct WebDriver for your browser, e.g., chromedriver for Chrome)
driver = webdriver.Firefox()

# Open the Google homepage
driver.get("https://www.google.com")

# Wait for the spacebar press
print("Press the spacebar to start actions.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Keep the browser open for a while to see the actions
time.sleep(10)

# Close the browser
driver.quit()
