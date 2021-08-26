import pytest
import allure

from selenium import webdriver, common


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--executor", action="store", default="localhost")
    parser.addoption("--bversion", action="store", default="92.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)
    parser.addoption("--mobile", action="store_true")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--bversion")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    videos = request.config.getoption("--videos")
    mobile = request.config.getoption("--mobile")

    if executor == "local":
        caps = {'goog:chromeOptions': {}}

        if mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

        wd = webdriver.Chrome(desired_capabilities=caps)

    else:
        executor_url = f"http://{executor}:4444/wd/hub"

        caps = {
            "browserName": browser,
            "browserVersion": version,
            "screenResolution": "1280x1024",
            "name": "agr tests",
            "selenoid:options": {
                "sessionTimeout": "60s",
                "enableVNC": vnc,
                "enableVideo": videos,
                "enableLog": logs
            },
            # 'goog:chromeOptions': {}
        }

        if browser == "chrome" and mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

        wd = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps
        )

        if not mobile:
            wd.maximize_window()

    @allure.step("Check page title contains {target}")
    def check_in_title(target):
        assert target in wd.title

    @allure.step("Verify element {css_selector} on page.")
    def check_element_presence(driver, css_selector):
        try:
            driver.find_element_by_css_selector(css_selector)
        except common.exceptions.NoSuchElementException:
            allure.attach(
                name=driver.session_id,
                body=driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Element {css_selector} not found on page!")

    wd.check_in_title = check_in_title
    wd.check_element_presence = check_element_presence

    def fin():
        wd.quit()

    request.addfinalizer(fin)
    return wd
