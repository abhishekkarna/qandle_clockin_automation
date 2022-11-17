from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.helpers import check_if_today_is_holiday, get_clock_in_button
from utils.custom_logging import logger as logging
from utils.constants import ZIGRAM_LOGIN_URL, ZIGRAM_HOME_PAGE_URL
from dotenv import load_dotenv
import time
import os
from datetime import datetime
from random import randint
load_dotenv()

browser = webdriver.Chrome()
EMAIL = os.environ.get("email")
PASSWORD = os.environ.get("password")
clock_in_button = None

if __name__ == '__main__':
    if None in (EMAIL,PASSWORD):
        logging.error("Email/password is missing in .env file")
        exit(0)
    logging.info("Opening zigram qandle")
    browser.get(ZIGRAM_LOGIN_URL)
    email = browser.find_element(By.ID, "input_1")
    password = browser.find_element(By.ID, "input_0")
    email.send_keys(EMAIL)
    password.send_keys(PASSWORD)
    logging.info("Logging into qandle")
    browser.find_element(By.TAG_NAME, "button").click()
    clock_in_button = get_clock_in_button(browser)
    is_holiday,reason = check_if_today_is_holiday(browser)
    logging.info(f"Is holoiday response : {is_holiday} and reason {reason}")
    if not is_holiday:
        browser.get(ZIGRAM_HOME_PAGE_URL)
        clock_in_button = get_clock_in_button(browser)
        if not clock_in_button:
            logging.error("Could not find clock in button")
        else:
            file_name = datetime.now().strftime("%Y-%m-%d")
            logging.info("Clocking in now")
            logging.info(f"Clock in button element {clock_in_button}")
            browser.save_screenshot(f'screenshots/{file_name}-clocking-in.png')
            browser.execute_script("arguments[0].removeAttribute('disabled')", clock_in_button)
            # time.sleep(randint(10,100))
            clock_in_button.click()
            time.sleep(3)
            logging.info("Clocked in")
            browser.save_screenshot(f'/screenshots/{file_name}-clocked-in.png')