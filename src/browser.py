import platform

from typing import Any, Generator
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver


def build_browser() -> WebDriver | None:
    """
    Builds a Selenium webdriver instance
    """
    print("Instantiating webdriver instance..")

    # The webdriver chromium headless instance
    c_options = ChromeOptions()
    try:
        if "Windows" in platform.platform():
            c_options.add_argument("--headless")
            c_options.add_argument("--no-sandbox")
            c_options.add_argument("--disable-dev-shm-usage")
            _browser = webdriver.Chrome(options=c_options)
        elif "macOS" in platform.platform():
            f_options = FirefoxOptions()
            f_options.add_argument("-headless")
            _browser = webdriver.Firefox(
                options=f_options,
                service=FirefoxService("/opt/homebrew/bin/geckodriver"),
            )
        else:
            c_options.add_argument("--no-sandbox")
            c_options.add_argument("--disable-dev-shm-usage")
            c_options.add_argument("--headless")
            c_options.add_argument("disable-infobars")
            _browser = webdriver.Chrome(
                options=c_options,
                service=ChromeService("/usr/bin/chromedriver"),
            )
        return _browser
    except ValueError:
        print(
            "Failed to setup Selenium, this is most likely an issue with unsupported OS."
        )
        return None


@contextmanager
def get_selenium_browser() -> Generator[WebDriver, Any, Any]:
    """
    A context manager that provides a Selenium webdriver instance for functions requiring it
    and also makes sure that the webdriver gets closed properly after being used.
    """
    _browser = build_browser()

    if _browser is None:
        raise ValueError("Failed to instantiate Selenium webdriver instance.")
    else:
        try:
            yield _browser
        finally:
            _browser.quit()
