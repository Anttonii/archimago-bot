import typer

import src.curiosa as curiosa
import src.util as util
from src import DiscordClient, Trie, with_selenium

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
    return


@app.command()
def download(output: str = "data"):
    """
    Downloads card data from the official curiosa.io API and saves it into a file.
    """
    curiosa.download_cards_json(output)


def command_preq(card_name: list[str]) -> tuple[str, Trie, dict]:
    """
    Shorthand for initializing card name suggestions in commands
    """
    cards = util.load_cards()

    return (
        util.get_card_name_url_form(" ".join(card_name)),
        Trie(util.get_all_card_names(cards)),
        cards,
    )


if __name__ == "__main__":
    app()
