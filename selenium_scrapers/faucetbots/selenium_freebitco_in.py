from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import logging
import os
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
dotenv_path = "/app/.env"  # Adjust the path if necessary
load_dotenv(dotenv_path)

# Get the credentials from the environment variables
EMAIL = os.getenv('freebitco_in_email')
PASSWORD = os.getenv('freebitco_in_password')

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG level for detailed logs
logger = logging.getLogger(__name__)

# Path to your geckodriver
gecko_driver_path = "/usr/local/bin/geckodriver"

# Initialize Firefox options
firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference("dom.webnotifications.enabled", False)
firefox_options.set_preference("dom.push.enabled", False)
firefox_options.set_preference("privacy.trackingprotection.enabled", True)

# Initialize the WebDriver Service
service = FirefoxService(gecko_driver_path)

# Function to handle the cookie consent
def handle_cookie_consent(driver):
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/a[1]"))
        )
        driver.execute_script("arguments[0].click();", cookie_button)
        logger.info("Clicked the cookie consent button using JavaScript")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.info(f"Cookie consent button not found or not clickable: {e}")

# Function to handle the first banner
def handle_first_banner(driver):
    try:
        banner_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[14]/div[1]/div[2]/div/div[1]"))
        )
        driver.execute_script("arguments[0].click();", banner_button)
        logger.info("Clicked the first banner's deny button using JavaScript")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.info(f"First banner not found or not clickable: {e}")

# Function to navigate to the website
def navigate_to_login_page(driver):
    driver.get("https://freebitco.in/")
    handle_cookie_consent(driver)
    handle_first_banner(driver)
    try:
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.login_menu_button a"))
        )
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Clicked the LOGIN button using JavaScript")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.error(f"Login button not found: {e}", exc_info=True)

# Function to login
def login(driver):
    try:
        # Wait for the login form to be visible
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "login_form"))
        )
        logger.info("Login form is visible")

        # Wait for the login elements to load
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "login_form_btc_address"))
        )
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "login_form_password"))
        )
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "login_button"))
        )
        logger.info("Login elements located")

        # Ensure elements are interactable
        driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
        driver.execute_script("arguments[0].scrollIntoView(true);", password_field)
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
        logger.info("Elements scrolled into view")

        # Enter login credentials
        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)
        driver.execute_script("arguments[0].click();", login_button)
        logger.info("Login form submitted using JavaScript")

        # Wait for the login process to complete
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "FREE BTC"))
        )
        logger.info("Login process complete")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        logger.error(f"An error occurred during login: {e}", exc_info=True)

    finally:
        # Function to dismiss the banner that pops up after login
        try:
            banner = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/a"))
            )
            driver.execute_script("arguments[0].click();", banner)
            logger.info("Closed the banner using JavaScript")
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            logger.info(f"Banner not found or not clickable: {e}")

# Function to log earnings
def log_earnings(session_start_balance, session_end_balance):
    earnings = float(session_end_balance) - float(session_start_balance)
    log_entry = f"Session Earnings: {earnings} BTC (Start: {session_start_balance}, End: {session_end_balance})\n"
    with open("btc_earnings_log.txt", "a") as log_file:
        log_file.write(log_entry)
    logger.info(log_entry)

# Function to wait until the next roll
def wait_until_next_roll(driver):
    while True:
        try:
            roll_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[7]/p[3]/input"))
            )
            logger.info("Roll button located")

            # Scroll into view and ensure the button is interactable
            driver.execute_script("arguments[0].scrollIntoView(true);", roll_button)
            time.sleep(2)  # Adding a slight delay to ensure the element is interactable
            driver.execute_script("arguments[0].click();", roll_button)
            logger.info("Clicked the ROLL! button using JavaScript")

            initial_balance = driver.find_element(By.CSS_SELECTOR, "span#balance").text
            logger.debug(f"Initial balance: {initial_balance}")

            WebDriverWait(driver, 60).until(
                lambda driver: driver.find_element(By.CSS_SELECTOR, "span#balance").text != initial_balance
            )
            new_balance = driver.find_element(By.CSS_SELECTOR, "span#balance").text
            logger.info(f"New balance: {new_balance}")

            if initial_balance != new_balance:
                logger.info("Balance has changed successfully")
                log_earnings(initial_balance, new_balance)
            else:
                logger.warning("Balance did not change")

            try:
                additional_banner = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/a"))
                )
                driver.execute_script("arguments[0].click();", additional_banner)
                logger.info("Closed the additional banner using JavaScript")
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                logger.info(f"Additional banner not found or not clickable: {e}")

            time.sleep(3900)
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
            logger.error(f"An error occurred: {e}", exc_info=True)

# Initialize the WebDriver only once
try:
    driver = webdriver.Firefox(service=service, options=firefox_options)
    logger.info("WebDriver initialized successfully.")
    navigate_to_login_page(driver)
    login(driver)

    while True:
        try:
            wait_until_next_roll(driver)
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)

finally:
    driver.quit()
    logger.info("Driver quit successfully.")
