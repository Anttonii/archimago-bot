from typing import Any

import json
import os
import platform
import re

import chromedriver_autoinstaller
from discord import DMChannel, GroupChannel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
import toml


def build_browser():
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
            c_options.add_argument("--headless=old")
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


def load_cards(json_path: str = "data/cards.json"):
    """
    Loads cards from cards.json into memory for quick retrieval.
    """
    if not os.path.exists(json_path):
        raise Exception(
            f"Failed to load cards.json from path: {json_path}, file not found."
        )

    with open(json_path, "r", encoding="utf-8") as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            print(
                f"Failed to load {json_path}, the file at path is an invalid JSON file."
            )
            return None

    return data


def load_terms(toml_path: str = "data/terms.toml"):
    """
    Parse keywords and their explanations from keywords TOML.
    """
    if not os.path.exists(toml_path):
        raise Exception(
            f"Failed to load keywords.toml from path: {toml_path}, file not found."
        )

    try:
        parsed_toml = toml.load(toml_path)
        return parsed_toml
    except TypeError:
        return None


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


def get_card_name_url_form(card_name: str) -> str:
    """
    Converts card name to lower case, replaces spaces with underscores and removes special characters.
    """
    special_chars = ["'", "!"]

    card_name = card_name.lower()
    card_name = card_name.replace(" ", "_")
    card_name = card_name.replace("-", "_")  # Dream-Quest, Wills-o-the-Wisp

    # Remove special characters
    for c in special_chars:
        card_name = card_name.replace(c, "")

    return card_name


def parse_sets(card):
    """
    Parses sets into a single line
    """
    output = ""
    sets = card["sets"]

    for _set in sets:
        output += _set["name"] + ", "

    return output[0 : len(output) - 2]


def parse_threshold(guardian):
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


def get_card_entry(card_name: str, cards: dict | None) -> Any | None:
    """
    Gets the card object from given card dictionary.
    """
    # Load cards if a proper dictionary object is not provided
    if cards is None:
        cards = load_cards()

    assert cards is not None

    for card in cards:
        if get_card_name_url_form(card["name"]) == get_card_name_url_form(card_name):
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


def get_all_card_names(cards: dict):
    """
    Extracts all card names from a cards dictionary file.
    """
    assert cards is not None

    return [get_card_name_url_form(card["name"]) for card in cards]


def with_selenium(func):
    """
    A decorator that provides a Selenium webdriver instance for functions requiring it
    and also makes sure that the webdriver gets closed properly after being used.
    """

    def inner1(*args):
        _browser = build_browser()

        if _browser is None:
            print("Failed to instantiate Selenium webdriver instance.")
            return

        func(*args, _browser)

        _browser.quit()

    return inner1


def contains_regex(s: str, p: list[str]) -> bool:
    """
    Checks if string contains some regex pattern.
    """
    for pattern in p:
        reg = re.compile(pattern)
        if reg.search(s):
            return True
    return False
