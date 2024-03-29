from time import sleep
from selenium.webdriver.common.keys import Keys


def test_google(driver):
    driver.get("https://google.ru")
    driver.check_in_title("Google")
    input = driver.find_element_by_css_selector("textarea")
    input.send_keys("Selenoid")
    input.send_keys(Keys.RETURN)
    driver.check_in_title("Selenoid")


def test_yandex(driver):
    driver.get("https://ya.ru")
    driver.check_element_presence("input[id='text']")
    driver.check_in_title("Яндекс")
