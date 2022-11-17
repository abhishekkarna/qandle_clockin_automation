from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.constants import DELAY, ZIGRAM_CALENDAR_URL
from utils.custom_logging import logger as logging

def check_if_today_is_holiday(browser):
    """
    Check if current day is a holiday or a weekend
    """
    browser.get(ZIGRAM_CALENDAR_URL)
    calendar_today = None
    try:
        calendar_today = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, "cal-day-today")))
    except TimeoutException:
        logging.error("Calendar load took so much time")
    else:
        logging.info(f"calendar_today {calendar_today}")
        classes = calendar_today.get_attribute("class").split()
        logging.info(f"Classes available {classes}")
        if "cal-day-weekend" in classes:
            # Weekend
            return True,"Weekend"
        else:
            badge_today = calendar_today.find_element(By.CLASS_NAME,"cal-events-num")
            badge_value = badge_today.get_attribute("textContent").strip()
            logging.info(f"badge_value {badge_value} and type={type(badge_value)}")
            badge_value_int = None
            try:
                badge_value_int = int(badge_value)
            except ValueError:
                logging.error("Exception while converting badge value to integer. Continuing")
            else:
                if badge_value_int is not None and badge_value_int > 0:
                    return True, "Holiday/Leave"
    return False, None

def get_clock_in_button(browser):
    """
    Returns the instance of clock in button
    """
    try:
        clock_in_button = WebDriverWait(browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Clock In']")))
    except TimeoutException:
        logging.error("Loading took too much time!")
        return None
    return clock_in_button