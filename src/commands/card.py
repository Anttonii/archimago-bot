from . import BaseCommand

from src.trie import Trie
import src.util as util
import src.curiosa as curiosa


class CardCommand(BaseCommand):
    def __init__(self, command: list[str], pt: Trie, cards: dict):
        self.pt = pt
        self.cards = cards

        super().__init__(command)

    def get_content(self, msg, parameters) -> str:
        """
        Get card data by providing a card name.
        """
        card_name = util.get_card_name_url_form(" ".join(parameters))

        # Safe to assume cards is not none here since we exit if it is
        received_output = curiosa.get_card_from_name(card_name, self.pt, self.cards)

        return util.code_blockify(received_output)
