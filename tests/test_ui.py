from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_google(driver):
    driver.get("https://google.ru")
    driver.check_in_title("Google")
    search_input = driver.find_element_by_css_selector(
        "input[type='text']")

    text = "Selenoid"
    search_input.send_keys(text)
    search_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(
        EC.title_contains(text)
    )
    driver.check_in_title(text)


def test_yandex(driver):
    driver.get("https://ya.ru")
    driver.check_element_presence("#text")
    driver.check_element_presence("a[title='Яндекс']")
    driver.check_in_title("Яндекс")
