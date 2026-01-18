import typer

import src.curiosa as curiosa
from src.util import (
    get_all_card_names,
    get_selenium_browser,
    download_cards_json,
    load_cards,
    get_url_form,
)
from src.discord_client import DiscordClient
from src.trie import Trie

# Typer instance
app = typer.Typer()


@app.command()
def discord():
    """
    Starts the discord bot.
    """
    dclient = DiscordClient()
    with get_selenium_browser() as browser:
        dclient.start_client(browser)


@app.command()
def overlap(ids: str):
    """
    Returns a list of cards that overlap in a list of decks. Does not support maybeboards
    """
    with get_selenium_browser() as browser:
        print(curiosa.get_overlapping_cards_from_str(ids, browser))


@app.command()
def url(url: str, include_maybe: bool = False):
    """
    Returns a deck of cards from an URL
    """
    with get_selenium_browser() as browser:
        print(curiosa.get_deck_from_url(url, browser))


@app.command()
def id(id: str, include_maybe: bool = False):
    """
    Returns a deck of cards from an ID.
    """
    with get_selenium_browser() as browser:
        print(curiosa.get_deck_from_id(id, browser, include_maybe))


@app.command()
def card(card_name: list[str]):
    """
    Gets a card by name and returns information associated with it.
    """
    cn, pt, cards = command_preq(card_name)
    print(curiosa.get_card_from_name(cn, pt, cards))


@app.command()
def faq(card_name: list[str]):
    """
    Gets a cards FAQ fields scraped from Curiosa.io
    """
    cn, pt, cards = command_preq(card_name)
    print(curiosa.get_faq_entries(cn, pt, cards))


@app.command()
def download(output: str = "data"):
    """
    Downloads card data from the official curiosa.io API and saves it into a file.
    """
    download_cards_json(output)


def command_preq(card_name: list[str]) -> tuple[str, Trie, dict]:
    """
    Shorthand for initializing card name suggestions in commands
    """
    cards = load_cards()

    return (
        get_url_form(" ".join(card_name)),
        Trie(get_all_card_names(cards)),
        cards,
    )


if __name__ == "__main__":
    app()
