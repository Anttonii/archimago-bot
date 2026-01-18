import json
import os
import platform
import re
import tomllib
from pathlib import Path
from typing import Any, Generator

from contextlib import contextmanager
import chromedriver_autoinstaller
import requests
from discord import DMChannel, GroupChannel
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

    # Checks if chrome driver is already in path, if not installs and adds it to path.
    if "macOS" not in platform.platform():
        chromedriver_autoinstaller.install()

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
            _browser = webdriver.Chrome(
                options=c_options,
                service=ChromeService("/snap/bin/chromium.chromedriver"),
            )
        return _browser
    except ValueError:
        print(
            "Failed to setup Selenium, this is most likely an issue with unsupported OS."
        )
        return None


def download_cards_json(
    output: str = "data", api_url="https://api.sorcerytcg.com/api/cards"
) -> bool:
    """
    Makes a request to Curiosa.io API to download the official card data.

    Returns whether or not the download was successful.
    """
    print(f"Retrieving sorcery card json file from {api_url}..")

    req = requests.get(api_url)
    req.raise_for_status()

    if req.status_code != 200:
        print(f"Failed to get cards API with status code: {req.status_code}")
        return False

    output_path = Path(output) / "cards.json"
    content = req.content.decode("utf-8")

    if not is_json(content):
        print(
            "The requested path did not provide valid json, can not save to file."
        )
        return False

    if output_path.exists():
        print("Cards.json already present, overwriting..")

    with open(output_path, "w+", encoding="utf-8") as json_file:
        json_file.write(content)

    print(f"Card data successfully downloaded and saved into: {output_path}!")
    return True


def load_cards(json_path: str = "data/cards.json") -> dict:
    """
    Loads cards from cards.json into memory for quick retrieval.
    """
    if not os.path.exists(json_path):
        print(f"{json_path} not found, attempting to download the json file.")

        if not download_cards_json():
            raise Exception("Attempt to download .json file failed.")

    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data


def load_toml(toml_path: Path) -> dict[str, Any]:
    """
    Parse toml file into a dictionary.
    """
    if not os.path.exists(toml_path):
        raise Exception(
            f"Failed to load toml file from path: {toml_path}, file not found."
        )

    with open(toml_path, "rb") as toml_file:
        return tomllib.load(toml_file)


def is_json(value: str) -> bool:
    """
    Checks if string is a valid json.
    """
    try:
        json.loads(value)
    except ValueError as e:
        print(f"Failed to load JSON from {value}, error: {e}")
        return False
    return True


def code_blockify(message: str) -> str:
    """
    Turns a string into a code block for discord
    """
    return "```" + message + "```"


def boldify(message: str) -> str:
    """
    Bolds a string for discord
    """
    return "**" + message + "**"


def message_truncate(message: str, preserve: int) -> str:
    """
    Utility function that truncates message into dicords max character limit of 2000.
    """
    # Removes all lettes after 2000 and replaces last 3 with dots
    # preserve value can be set so that we preserve more space, for example when using code_blockify.
    if len(message) > 2000:
        message = message[0 : 1997 - preserve]
        message += "..."

    return message


def get_url_form(text: str) -> str:
    """
    Converts text to lower case, replaces spaces with underscores and removes special characters.
    """
    special_chars = ["'", "!"]

    text = text.lower()
    text = text.replace(" ", "_")
    text = text.replace("-", "_")  # Dream-Quest, Wills-o-the-Wisp

    # Remove special characters
    for c in special_chars:
        text = text.replace(c, "")

    return text


def parse_sets(card):
    """
    Parses sets into a single line
    """
    output = ""
    sets = card["sets"]

    for _set in sets:
        output += _set["name"] + ", "

    return output[0 : len(output) - 2]


def parse_threshold(guardian) -> str:
    """
    Parses thresholds object into a more readable form.

    Example output for a card having 1 air and 1 water threshold is (A)(W)
    """
    output = ""
    thresholds = guardian["thresholds"]
    for k, v in thresholds.items():
        if v == 0:
            continue

        output += ("(" + k[0].capitalize() + ")") * v
    return output


def get_card_entry(card_name: str, cards: dict = load_cards()) -> Any | None:
    """
    Gets the card object from given card dictionary.
    """
    assert cards is not None

    for card in cards:
        if get_url_form(card["name"]) == get_url_form(card_name):
            return card

    return None


def check_channel(ctx) -> bool:
    """
    Checks if the channel is a private channel or group channel

    Used so that blocking requests are only made from servers
    """
    if isinstance(ctx, DMChannel) or isinstance(ctx, GroupChannel):
        return False

    return True


def get_all_card_names(cards: dict | None = None):
    """
    Extracts all card names from a cards dictionary file.
    """
    assert cards is not None

    return [get_url_form(card["name"]) for card in cards]


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


def contains_regex(s: str, p: list[str]) -> bool:
    """
    Checks if string contains some regex pattern.
    """
    for pattern in p:
        reg = re.compile(pattern)
        if reg.search(s):
            return True
    return False
