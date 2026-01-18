import json

from typing import Any

import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.util import get_card_entry, get_url_form, parse_threshold, parse_sets
from src.trie import Trie

# The curiosa.io base URL where deck requests are made to.
curiosa_deck_base_url = "https://curiosa.io/decks/"

# The curiosa.io base URL where card requests are made to.
curiosa_card_base_url = "https://curiosa.io/cards/"

# The maximum time to wait for a timeout in seconds
maximum_wait_timeout = 3


def prettify_deck(deck: dict[str, Any]) -> str:
    """
    Returns a more readable version of a given deck dictionary.
    """
    output = ""
    for k, v in deck.items():
        curr = ""
        sum = 0
        for e in v:
            curr += f"  {e[1]} - {e[0]}\n"
            sum += int(e[1])

        # Don't append empty groups
        if sum == 0:
            continue

        suffix = "" if k == "Avatar" else "s"
        curr = f"{k}{suffix} ({sum})\n" + curr
        output += curr

    return output + "\n"


def prettify_card(card) -> str:
    """
    Returns a more readable version of a given card dictionary entry.
    """
    output = "Name: " + card["name"] + "\n"

    guardian = card["guardian"]
    fields = [
        "rarity",
        "type",
        "rulesText",
        "cost",
        "attack",
        "defence",
        "life",
    ]

    thresholds = parse_threshold(guardian)
    sets = parse_sets(card)

    for field in fields:
        if guardian[field] == "" or guardian[field] is None:
            continue

        if field != "rulesText":
            output += field.capitalize() + ": " + str(guardian[field]) + "\n"
        else:
            output += "Rules Text: " + str(guardian[field]) + "\n"

    if thresholds != "":
        if guardian["type"] == "Site":
            output += "Provided thresholds: " + thresholds + "\n"
        else:
            output += "Thresholds: " + thresholds + "\n"

    # Assuming that sets field is never empty
    output += "Sets: " + sets + "\n"

    return output


def get_card_counts(deck) -> str:
    """
    Returns a string that represents a list of counts of different cards by their type.
    """
    output = ""
    total_sum = 0
    atlas_sum = 0

    for k, v in deck.items():
        if k == "Avatar":
            continue

        sum = 0
        for e in v:
            sum += int(e[1])
            if k == "Site":
                atlas_sum += int(e[1])
        total_sum += sum

    output += f"Total: {total_sum} cards({total_sum - atlas_sum} Spellbook, {atlas_sum} Atlas)\n\n"
    return output


def overlap_in_decks(*decks):
    """
    Returns a dictionary of overlapping cards between decks, all decks are compared against the first one.
    """
    base = decks[0]
    overlapping = {}
    for deck in decks[1 : len(decks)]:
        for k, v in deck.items():
            # To avoid finding the same overlaps
            found_overlaps = []

            if k not in overlapping:
                overlapping[k] = []

            if k not in base:
                continue

            for i, e in enumerate(overlapping[k]):
                for ve in v:
                    if ve[0] == e[0]:
                        overlapping[k][i] = (e[0], min(e[1], ve[1]))
                        found_overlaps.append(e[0])

            for e in base[k]:
                for ve in v:
                    if ve[0] == e[0] and ve[0] not in found_overlaps:
                        overlapping[k].append((ve[0], min(e[1], ve[1])))

    return overlapping


def parse_deck_table(tables: list[WebElement], include_maybe: bool = False):
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

        for line in lines[1 : len(lines)]:
            if len(line) == 1:  # skip over the mana cost lines
                continue
            deck[head].append((line[1 : len(line)], line[0]))

    return deck


def request_faq(card_name: str):
    """
    Requests a cards FAQ information and returns the corresponding FAQ information
    """
    url = curiosa_card_base_url + card_name

    req = requests.get(url)
    if req.status_code != 200:
        print(
            f"Failed to load FAQ for card name: {card_name}, status code: {req.status_code}"
        )
        return {"failed": "err_status_code"}

    soup = BeautifulSoup(req.content.decode("utf-8"), "html.parser")

    # Extract the script content that has the json we are looking for
    content = soup.find(id="__NEXT_DATA__").contents[0]  # type: ignore
    if content is None:
        return {"failed": "no_content"}

    content = content.contents[0]  # type: ignore
    card_json = json.loads(content)
    card_data = card_json["props"]["pageProps"]["trpcState"]["json"]["queries"][0][
        "state"
    ]["data"]

    if card_data is None:
        print(f"Failed to load FAQ for card name: {card_name}, card not found!")
        return {"failed": "not_found"}

    return card_data["faqs"]


def get_faq_entries(card_name: str, pt: Trie, cards: dict):
    """
    Makes a request for cards FAQ and returns it in string form if the request is successful
    """
    output = f"FAQ entries found for card: {card_name}\n\n"
    if get_card_entry(card_name, cards) is None:
        return get_content_suggestion(card_name, pt, "Could not find card by card name")

    faq = request_faq(card_name)
    if isinstance(faq, dict):
        return (
            f"Retrieving FAQ for card {card_name} failed with reason: {faq['failed']}"
        )

    if len(faq) == 0:
        return f"No FAQ entries found for card: {card_name}."

    for q in faq:
        output += "Q: " + q["question"] + "\n"
        output += "A: " + q["answer"] + "\n\n"

    return output.rstrip()


def request_deck(
    url: str, browser: WebDriver, include_maybe: bool = False
) -> dict[str, Any] | None:
    """
    Requests a deck from curiosa.io
    """
    try:
        print(f"Retrieving deck information from URL: {url}.")
        browser.get(url)

        WebDriverWait(browser, maximum_wait_timeout).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "div > table"))
        )
        try:
            tables = browser.find_elements(By.TAG_NAME, "table")
            return parse_deck_table(tables, include_maybe)
        except NoSuchElementException:
            print(
                f"Failed to retrieve element containing deck information for URL: {url}"
            )
    except TimeoutException:
        print("Request timed out.")

    return None


def request_deck_from_id(id: str, browser: WebDriver, include_maybe: bool = False):
    """
    Appends the base curiosa.io url and passes it into request_deck.
    """
    return request_deck(curiosa_deck_base_url + id, browser, include_maybe)


def get_overlapping_cards(ids, browser: WebDriver) -> str:
    output = ""
    decks = []

    for i, id in enumerate(ids):
        print(f"Requesting deck {i + 1} with id: {id}")
        decks.append(request_deck_from_id(id, browser, False))

    overlapping = overlap_in_decks(*decks)

    # No overlapping cards
    if not overlapping:
        output = "There are no overlapping cards."
    else:
        output += "The overlapping cards are:\n\n"
        output += prettify_deck(overlapping)

    return output


def get_overlapping_cards_from_str(ids: str, browser: WebDriver) -> str:
    return get_overlapping_cards(ids.split(" "), browser)


def get_deck_from_url(url: str, browser: WebDriver, include_maybe: bool = False) -> str:
    output = ""

    deck = request_deck(url, browser, include_maybe)
    if deck is None:
        output = f"Failed to load deck with url: {url}"
        output = "Check that the url is a valid one."
        return output

    output += f"The deck from url: {url} has the following cards:\n\n"
    output += prettify_deck(deck)
    output += get_card_counts(deck)

    return output


def get_deck_from_id(id: str, browser: WebDriver, include_maybe: bool = False) -> str:
    output = ""

    deck = request_deck_from_id(id, browser, include_maybe)
    if deck is None:
        output = f"Failed to load deck with id: {id}"
        output = "Check that the id is a valid one."
        return output

    output += f"The deck with id: {id} has the following cards:\n\n"
    output += prettify_deck(deck)
    output += get_card_counts(deck)

    return output


def get_card_from_name(card_name: str, pt: Trie, cards: dict) -> str:
    """
    Returns card information from given card name.
    """
    card = get_card_entry(card_name, cards)

    if card is None:
        return get_content_suggestion(card_name, pt, "Could not find card by card name")
    else:
        return prettify_card(card)


def generate_image_url(card_name: str, pt: Trie, cards: dict) -> str:
    """
    Generates an image URL from a given card name.
    """
    base_url = (
        "https://curiosa.io/_next/image?url=https://d27a44hjr9gen3.cloudfront.net/"
    )
    extension = "_b_s.png&w=384&q=75"

    card = get_card_entry(card_name, cards)
    if card is None:
        return get_content_suggestion(card_name, pt, "Could not find card by card name")

    card_name = get_url_form(card["name"])

    set = parse_sets(card)

    # Take the first set and the first 3 characters converted to lower case
    set_name = set[0:3].lower()

    return base_url + set_name + "/" + card_name + extension


def get_content_suggestion(content: str, pt: Trie, explanation: str) -> str:
    """
    Returns a string that gives suggestions when given some content.

    The suggestions are generated by the prefix tree associated with the content.

    Explanation parameter is used a prefix for the suggestion generated.
    """
    if pt is None:
        return f"Could not find card by card name {content}."

    prefixes = pt.starts_with(content)
    fuzzy = pt.fuzzy_match(content)

    if fuzzy is None:
        prefix = "." if prefixes is None else f", did you mean: {prefixes[0]}?"
    else:
        prefix = f", did you mean: {fuzzy[1]}?"

    return f"{explanation}: {content}{prefix}"
