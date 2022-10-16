from time import sleep

from django.conf import settings
from selenium.common.exceptions import ElementNotInteractableException, NoAlertPresentException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.env_utils import ENV


def get_chrome_instance(
        is_remote: bool = True,
        is_headless: bool = True,
        is_notifications_disabled: bool = True,
) -> WebDriver:
    """Returns some fancy options for selenium webdriver which makes the browser look like a real browser and not
    some bot.
    :param is_notifications_disabled:
    :param is_remote:
    :param is_headless:
    :return: a chrome webdriver instance
    """
    options = Options()

    if is_headless:
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    if is_notifications_disabled:
        options.add_argument("--disable-notifications")

    if settings.ENV == ENV.DEV:
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-notifications")

        # options = webdriver.ChromeOptions()
        # options.add_argument("--start-maximized")

    if is_remote:
        driver = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            options=options,
            desired_capabilities={
                "browserName": "chrome",
            },
        )
    else:
        driver = webdriver.Chrome(
            options=options,
        )
    return driver


def send_keys_to_element(element, keys):
    try:
        element.send_keys(keys)
    except ElementNotInteractableException:
        pass


def close_alert_pop_ups(
        dr,
        alert_preset_wait_in_seconds=0.25,
        post_alert_preset_wait_in_seconds=0.25,
        attempt_jumping_to_next_element=True
):
    try:
        if attempt_jumping_to_next_element:
            dr.switch_to.active_element.send_keys(Keys.TAB)
        WebDriverWait(dr, alert_preset_wait_in_seconds).until(EC.alert_is_present())
        dr.switch_to.alert.accept()
        sleep(post_alert_preset_wait_in_seconds)
    except (NoAlertPresentException, ElementNotInteractableException, TimeoutException):
        pass
