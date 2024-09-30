from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException
import logging
import os
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
dotenv_path = ".env"  # Adjust the path if necessary
load_dotenv(dotenv_path)

# Get the credentials from the environment variables
EMAIL = os.getenv('freebitco_in_email')
PASSWORD = os.getenv('freebitco_in_password')

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG level for detailed logs
logger = logging.getLogger(__name__)

# Path to your geckodriver
gecko_driver_path = "/usr/bin/geckodriver"

# Initialize Firefox options for headless mode
firefox_options = webdriver.FirefoxOptions()
#firefox_options.add_argument("--headless")  # Run in headless mode
firefox_options.set_preference("dom.webnotifications.enabled", False)
firefox_options.set_preference("dom.push.enabled", False)
firefox_options.set_preference("privacy.trackingprotection.enabled", True)

# Initialize the WebDriver Service
service = FirefoxService(gecko_driver_path)

# Function to dismiss the cookie consent banner if present
def dismiss_cookie_banner(driver):
    try:
        cookie_banner_xpath = "/html/body/div[1]/div/a[1]"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cookie_banner_xpath))
        )
        cookie_banner_button = driver.find_element(By.XPATH, cookie_banner_xpath)
        driver.execute_script("arguments[0].click();", cookie_banner_button)
        logger.info("Cookie banner dismissed successfully.")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.info("No cookie banner found or already dismissed.")

# Function to trigger the login form using Selenium
def trigger_login_form(driver):
    try:
        # Correct XPath to trigger the login form
        login_xpath = "/html/body/div[1]/div/nav/section/ul/li[10]/a"
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, login_xpath))
        )
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Login tab clicked successfully.")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.error(f"An error occurred while triggering the login form: {e}", exc_info=True)

# Function to login using Selenium
def login(driver):
    try:
        # Wait for the login form to be visible, ensure that the form is interactable
        login_form_xpath = "//*[@id='login_form']"
        WebDriverWait(driver, 20, poll_frequency=1).until(
            EC.visibility_of_element_located((By.XPATH, login_form_xpath))
        )
        logger.info("Login form is visible and interactable.")

        # Wait for the login elements to load
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_form_btc_address"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_form_password"))
        )
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login_button"))
        )
        logger.info("Login elements located.")

        # Enter login credentials
        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Login form submitted using JavaScript.")

        # Wait for the login process to complete
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/nav/section/ul/li[2]/a"))
        )
        logger.info("Login process complete.")
        
    except TimeoutException:
        logger.error("Timed out waiting for login elements.")
    except Exception as e:
        logger.error(f"An error occurred during login: {e}", exc_info=True)

# Function to check for countdown and roll
def check_countdown_and_roll(driver):
    try:
        # Check if countdown is active
        countdown_xpath = "//*[@id='time_remaining']"
        try:
            countdown = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, countdown_xpath))
            )
            time_remaining = countdown.text
            logger.info(f"Countdown active: {time_remaining}")
            return time_remaining
        except TimeoutException:
            logger.info("No countdown detected, attempting to roll.")
            return None
    except Exception as e:
        logger.error(f"An error occurred while checking the countdown: {e}", exc_info=True)

# Function to handle the "Play without Captcha" button and "ROLL" button
def roll_without_captcha(driver):
    try:
        # Click the "Play without Captcha" button
        play_without_captcha_xpath = "//*[@id='play_without_captchas_button']"
        play_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, play_without_captcha_xpath))
        )
        driver.execute_script("arguments[0].click();", play_button)
        logger.info("Clicked 'Play without Captcha' button.")

        # Click the "ROLL" button after triggering play without captcha
        roll_button_xpath = "//*[@id='free_play_form_button']"
        roll_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, roll_button_xpath))
        )
        driver.execute_script("arguments[0].click();", roll_button)
        logger.info("Successfully clicked the 'ROLL' button.")

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.error(f"An error occurred while trying to roll: {e}", exc_info=True)

# Main execution flow
if __name__ == '__main__':
    try:
        # Initialize the WebDriver
        driver = webdriver.Firefox(service=service, options=firefox_options)
        logger.info("WebDriver initialized successfully.")
        
        # Navigate to the page
        driver.get("https://freebitco.in")
        
        # Dismiss the cookie consent banner if present
        dismiss_cookie_banner(driver)
        
        # Trigger the login tab
        trigger_login_form(driver)
        
        # Proceed with the login process
        login(driver)
        
        while True:
            # Check if there's a countdown or we can roll
            countdown = check_countdown_and_roll(driver)
            
            if countdown:
                # If a countdown is active, wait and check again after a while
                logger.info(f"Waiting for countdown: {countdown}. Checking again in 5 minutes.")
                time.sleep(300)  # Sleep for 5 minutes before checking again
            else:
                # Attempt to perform the roll action
                roll_without_captcha(driver)
                logger.info("Waiting for the next roll. Checking in 60 minutes.")
                time.sleep(3600)  # Sleep for 1 hour before checking again

    except WebDriverException as e:
        logger.error(f"An error occurred with the WebDriver: {e}", exc_info=True)

    finally:
        if 'driver' in locals():
            driver.quit()
            logger.info("Driver quit successfully.")
