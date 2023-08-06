from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scroll(driver, start: int, end: int):
    driver.execute_script('window.scrollTo({},{});'.format(start, end))


def screen_shot(driver, filename):
    driver.get_screenshot_as_file(filename)


def click_by_xpath(driver, xpath: str):
    click(driver, driver.find_element_by_xpath(xpath))


def click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def wait_element(driver, xpath: str,
                 timeout_seconds: int = 10,
                 frequency: float = 0.5):
    return WebDriverWait(driver, timeout_seconds, frequency).until(
        EC.presence_of_element_located((By.XPATH, xpath)))


def has_element(driver, xpath: str):
    try:
        e = driver.find_element_by_xpath(xpath)
        return True, e
    except NoSuchElementException:
        return False, None
