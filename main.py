import src.util as util
import src.curiosa as curiosa
from src import DiscordClient

from src.util import with_selenium

from typing import List

import typer

# Typer instance
app = typer.Typer()


@with_selenium
def _discord(browser=None):
    dclient = DiscordClient()
    dclient.start_client(browser)


@app.command()
def discord():
    """
    Starts the discord bot.
    """
    _discord()


@with_selenium
def _overlap(ids: str, browser=None):
    print(curiosa.get_overlapping_cards_from_str(ids, browser))


@app.command()
def overlap(ids: str):
    """
    Returns a list of cards that overlap in a list of decks. Does not support maybeboards
    """
    _overlap(ids)


@with_selenium
def _url(url: str, include_maybe: bool = False, browser=None):
    print(curiosa.get_deck_from_url(url, include_maybe, browser))


@app.command()
def url(url: str, include_maybe: bool = False):
    """
    Returns a deck of cards from an URL
    """
    _url(url, include_maybe)


@with_selenium
def _id(id: str, include_maybe: bool = False, browser=None):
    print(curiosa.get_deck_from_id(id, include_maybe, browser))


@app.command()
def id(id: str, include_maybe: bool = False):
    """
    Returns a deck of cards from an ID.
    """
    _id(id, include_maybe)


@app.command()
def card(card_name: List[str]) -> str:
    """
    Gets a card by name and returns information associated with it.
    """
    print(curiosa.get_card_from_name(" ".join(card_name)))


@app.command()
def faq(card_name: List[str]) -> str:
    print(curiosa.get_faq_entries(util.get_card_name_url_form(' '.join(card_name))))


@app.command()
def download(output: str = 'data'):
    """
    Downloads card data from the official curiosa.io API and saves it into a file.
    """
    curiosa.download_cards_json(output)


if __name__ == "__main__":
    app()
