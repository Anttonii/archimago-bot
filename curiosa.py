from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

import typer

# The curiosa.io base URL where deck requests are made to.
curiosa_deck_base_url = "https://curiosa.io/decks/"

# The maximum time to wait for a timeout in seconds
maximum_wait_timeout = 3

# The path to the chrome driver to use with selenium
chromedriver_path = 'driver/chromedriver.exe'

# Typer instance
app = typer.Typer()

# The webdriver chromium headless instance
options = Options()
options.add_argument('--headless=old')

# Create a headless Chromium browser
browser = webdriver.Chrome(
    options=options, service=Service('driver/chromedriver.exe'))


def prettify_deck(deck):
    """
    Prints a more readable version of a given deck dictionary.
    """
    output = ""
    for (k, v) in deck.items():
        output += f"{k}{"" if k == "Avatar" else "s"}\n"
        for e in v:
            output += f"  {e[1]} - {e[0]}\n"
    return output


def get_card_counts(deck):
    """
    Prints a list of counts of different cards by their type
    """
    output = ""
    total_sum = 0
    for (k, v) in deck.items():
        sum = 0
        for e in v:
            sum += int(e[1])
        output += f"{k}{"s" if sum > 1 else ""}: {sum}\n"
        total_sum += sum
    output += f"Total of {total_sum} cards\n\n"
    return output


def overlap_in_decks(*decks):
    """
    Returns a dictionary of overlapping cards between decks, all decks are compared against the first one.
    """
    base = decks[0]
    overlapping = {}
    for deck in decks[1:len(decks)]:
        for (k, v) in deck.items():
            found_overlaps = []
            if k not in overlapping:
                overlapping[k] = []

            if k not in base:
                continue

            for (i, e) in enumerate(overlapping[k]):
                for ve in v:
                    if ve[0] == e[0]:
                        overlapping[k][i] = (e[0], min(e[1], ve[1]))
                        found_overlaps.append(e[0])

            for e in base[k]:
                for ve in v:
                    if ve[0] == e[0] and ve[0] not in found_overlaps:
                        overlapping[k].append((ve[0], min(e[1], ve[1])))

    return overlapping


def parse_deck_table(tables, include_maybe=False):
    """
    Parses the table element returned by selenium into a dictionary that contains all cards.
    """
    deck = {}

    # Parse table head
    for table in tables:
        table_content = table.text
        lines = table_content.split("\n")

        head = lines[0].split(" ")[0]

        # Ignore maybeboard option
        if head == "Maybeboard" and not include_maybe:
            continue

        if head not in deck:
            deck[head] = []

        for line in lines[1:len(lines)]:
            if len(line) == 1:  # skip over the mana cost lines
                continue
            deck[head].append((line[1:len(line)], line[0]))

    return deck


def request_deck(browser: webdriver.Chrome, url: str, include_maybe: bool = False):
    """
    Requests a deck from curiosa.io
    """
    try:
        browser.get(url)
        WebDriverWait(browser, maximum_wait_timeout).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "div > table")))
        tables = browser.find_elements(By.TAG_NAME, "table")
        return parse_deck_table(tables, include_maybe)
    except TimeoutException:
        print("Request timed out.")
        return None


def request_deck_from_id(browser, id: str, include_maybe: bool = False):
    """
    Appends the base curiosa.io url and passes it into request_deck.
    """
    return request_deck(browser, curiosa_deck_base_url + id, include_maybe)


def get_overlapping_cards(browser: webdriver.Chrome, *ids: str) -> str:
    output = ""
    decks = []

    for (i, id) in enumerate(ids):
        print(f"Requesting deck {i+1} with id: {id}")
        decks.append(request_deck_from_id(browser, id, False))

    overlapping = overlap_in_decks(*decks)
    output += "The overlapping cards are:\n"
    output += prettify_deck(overlapping)

    return output


def get_overlapping_cards_from_str(browser: webdriver.Chrome, ids: str) -> str:
    return get_overlapping_cards(ids.split(" "))


@app.command()
def overlap(ids: str):
    """
    Returns a list of cards that overlap in a list of decks. Does not support maybeboards
    """
    print(get_overlapping_cards_from_str(browser, ids))


def get_deck_from_url(browser: webdriver.Chrome, url: str, include_maybe: bool = False) -> str:
    output = ""

    deck = request_deck(browser, url, include_maybe)
    if deck == None:
        output = f"Failed to load deck with url: {url}"
        output = "Check that the url is a valid one."
        return output

    output += f"The deck from url: {url} has the following cards:\n"
    output += prettify_deck(deck)
    output += "\nand the following distribution:\n"
    output += get_card_counts(deck)

    return output


@app.command()
def url(url: str, include_maybe: bool = False):
    """
    Returns a deck of cards from an URL
    """
    print(get_deck_from_url(browser, url, include_maybe))


def get_deck_from_id(browser: webdriver.Chrome, id: str, include_maybe: bool = False) -> str:
    output = ""

    deck = request_deck_from_id(browser, id, include_maybe)
    if deck == None:
        output = f"Failed to load deck with id: {id}"
        output = "Check that the id is a valid one."
        return output

    output += f"The deck with id: {id} has the following cards:\n\n"
    output += prettify_deck(deck)
    output += "\nand the following distribution:\n\n"
    output += get_card_counts(deck)

    return output


@app.command()
def id(id: str, include_maybe: bool = False):
    """
    Returns a deck of cards from an ID.
    """
    print(get_deck_from_id(browser, id, include_maybe))


if __name__ == "__main__":
    app()
    browser.quit()
