from . import BaseCommand

from src.trie import Trie
import src.util as util
import src.curiosa as curiosa


class CardCommand(BaseCommand):
    """
    Get information about a card by providing a card name.
    """

    def __init__(self, command: list[str], pt: Trie, cards: dict):
        self.pt = pt
        self.cards = cards

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Usage:

        !card <card_name> returns information about given card name.
        """
        card_name = util.get_url_form(" ".join(parameters))

        # Safe to assume cards is not none here since we exit if it is
        received_output = curiosa.get_card_from_name(card_name, self.pt, self.cards)

        return util.code_blockify(received_output)
